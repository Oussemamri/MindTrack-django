from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from .models import LearningPath, PathTopic, PathEnrollment
from .forms import LearningPathForm, PathTopicFormSet
from quiz_app.models import Quiz
from .ai_helper import SimpleAI

@login_required
def path_list(request):
    paths = LearningPath.objects.all()
    user_enrollments = PathEnrollment.objects.filter(user=request.user)
    return render(request, 'learning_paths/path_list.html', {
        'paths': paths,
        'user_enrollments': user_enrollments
    })

@login_required
def create_path(request):
    if request.method == 'POST':
        form = LearningPathForm(request.POST)
        formset = PathTopicFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                path = form.save(commit=False)
                path.creator = request.user
                path.save()
                formset.instance = path
                formset.save()
            messages.success(request, 'Learning path created successfully!')
            return redirect('learning_paths:path_detail', path_id=path.id)
    else:
        form = LearningPathForm()
        formset = PathTopicFormSet(queryset=PathTopic.objects.none())
    
    return render(request, 'learning_paths/create_path.html', {
        'form': form,
        'formset': formset,
        'is_create': True,
        'form_errors': form.errors,
        'formset_errors': formset.errors if hasattr(formset, 'errors') else None
    })

@login_required
def edit_path(request, path_id):
    path = get_object_or_404(LearningPath, id=path_id, creator=request.user)
    if request.method == 'POST':
        form = LearningPathForm(request.POST, instance=path)
        formset = PathTopicFormSet(request.POST, instance=path)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                path = form.save()
                formset.save()
            messages.success(request, 'Learning path updated successfully!')
            return redirect('learning_paths:path_detail', path_id=path.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LearningPathForm(instance=path)
        formset = PathTopicFormSet(instance=path)
    
    return render(request, 'learning_paths/edit_path.html', {
        'form': form,
        'formset': formset,
        'path': path,
        'form_errors': form.errors,
        'formset_errors': formset.errors if hasattr(formset, 'errors') else None
    })

@login_required
def delete_path(request, path_id):
    path = get_object_or_404(LearningPath, id=path_id, creator=request.user)
    if request.method == 'POST':
        path.delete()
        messages.success(request, 'Learning path deleted successfully!')
        return redirect('learning_paths:path_list')
    return render(request, 'learning_paths/delete_path.html', {'path': path})

@login_required
def path_detail(request, path_id):
    path = get_object_or_404(LearningPath, id=path_id)
    user_enrolled = False
    user_progress = None
    
    if request.user.is_authenticated:
        user_enrolled = PathEnrollment.objects.filter(
            user=request.user,
            path=path
        ).exists()
        if user_enrolled:
            user_progress = PathEnrollment.objects.get(
                user=request.user,
                path=path
            )
    
    return render(request, 'learning_paths/path_detail.html', {
        'path': path,
        'user_enrolled': user_enrolled,
        'user_progress': user_progress
    })

@login_required
def enroll_path(request, path_id):
    path = get_object_or_404(LearningPath, id=path_id)
    
    if request.method == 'POST':
        # Check if user is already enrolled
        if not PathEnrollment.objects.filter(user=request.user, path=path).exists():
            # Get first topic in path
            first_topic = path.pathtopic_set.order_by('order').first()
            
            # Create enrollment
            PathEnrollment.objects.create(
                user=request.user,
                path=path,
                current_topic=first_topic
            )
            messages.success(request, f'You have successfully enrolled in {path.title}!')
        else:
            messages.warning(request, 'You are already enrolled in this path.')
            
    return redirect('learning_paths:path_detail', path_id=path_id)

def get_topic_quizzes(request, topic_id):
    quizzes = Quiz.objects.filter(topic_id=topic_id).values('id', 'title')
    return JsonResponse(list(quizzes), safe=False)

@login_required
def continue_path(request, path_id):
    path = get_object_or_404(LearningPath, id=path_id)
    enrollment = get_object_or_404(PathEnrollment, user=request.user, path=path)
    
    # If no current topic, get the first incomplete topic
    if not enrollment.current_topic:
        next_topic = path.pathtopic_set.order_by('order').first()
        if next_topic:
            enrollment.current_topic = next_topic
            enrollment.save()
    
    # If there's a current topic, redirect to its first incomplete quiz
    if enrollment.current_topic:
        for quiz in enrollment.current_topic.required_quizzes.all():
            best_attempt = quiz.attempts.filter(
                user=request.user
            ).order_by('-score').first()
            
            if not best_attempt or best_attempt.score < enrollment.current_topic.completion_threshold:
                return redirect(f"{reverse('quiz_app:take_quiz', args=[quiz.id])}?from_path={path_id}")
    
        # All quizzes in current topic are completed, move to next topic
        next_topic = path.pathtopic_set.filter(
            order__gt=enrollment.current_topic.order
        ).order_by('order').first()
        
        if next_topic:
            enrollment.current_topic = next_topic
            enrollment.save()
            return redirect('learning_paths:continue_path', path_id=path.id)
    
    # If no next topic, path is completed
    enrollment.completed_at = timezone.now()
    enrollment.save()
    messages.success(request, 'Congratulations! You have completed this learning path!')
    return redirect('learning_paths:path_detail', path_id=path.id)

@login_required
def dashboard(request):
    context = {
        'created_paths_count': LearningPath.objects.filter(creator=request.user).count(),
        'active_enrollments_count': PathEnrollment.objects.filter(
            user=request.user, 
            completed_at__isnull=True
        ).count(),
        'completed_paths_count': PathEnrollment.objects.filter(
            user=request.user, 
            completed_at__isnull=False
        ).count(),
        'created_paths': LearningPath.objects.filter(creator=request.user).order_by('-created_at')
    }
    return render(request, 'learning_paths/dashboard.html', context)

@login_required
def ai_assistant(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    user_input = request.POST.get('message', '')
    response = SimpleAI.get_response(user_input)
    return JsonResponse({'response': response})