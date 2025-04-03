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
    """AI Assistant view for learning path recommendations and Q&A."""
    
    # Get or initialize session chat history
    chat_history = request.session.get('chat_history', [])
    
    # Initialize context with default values
    context = {
        'chat_history': chat_history,
        'error': None,
        'suggested_questions': [
            "How can I learn Python programming?",
            "What are the best study techniques?",
            "Can you create a learning path for web development?",
            "Help me understand calculus basics",
            "What resources do you recommend for data science?"
        ]
    }
    
    # Process form submission (POST request)
    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        
        # Validate the query
        if not query:
            context['error'] = "Please enter a question or topic to get assistance."
        else:
            try:
                # Process greeting messages
                greeting_responses = {
                    "hi": "Hello! How can I help with your learning journey today?",
                    "hello": "Hi there! I'm your AI learning assistant. What would you like to learn about?",
                    "hey": "Hey! Ready to help you with your educational goals. What's on your mind?",
                    "hi there": "Hello! I'm here to help you learn. What topic are you interested in?",
                    "hello there": "Hi! I'm excited to assist with your learning. What can I help you with today?"
                }
                
                # Topic-specific canned responses
                ai_responses = {
                    "learn python": "To learn Python, I recommend starting with basic syntax and concepts like variables, data types, and control structures. Then move on to functions, classes, and modules. Practice with small projects like a calculator or a to-do list app.",
                    "study tips": "Some effective study techniques include: 1) Spaced repetition, 2) Active recall, 3) Pomodoro technique (25min study, 5min break), 4) Teaching concepts to others, and 5) Creating mind maps or visual aids.",
                    "math help": "For mathematics, build a strong foundation in basics before advancing. Use resources like Khan Academy for free lessons and practice problems. Consider joining study groups or finding a tutor for challenging topics.",
                    "learning path": "I can help create a learning path tailored to your goals. What specific field or topic are you interested in learning? For example, web development, data science, or a particular language?",
                    "web development": "For web development, I recommend starting with HTML/CSS basics, then learning JavaScript. After that, explore frontend frameworks like React or Vue, and backend technologies like Node.js, Django, or Flask.",
                    "data science": "To learn data science, start with Python programming, then study statistics and probability. Next, learn data manipulation with pandas, visualization with matplotlib/seaborn, and finally machine learning with scikit-learn."
                }
                
                # Check for greetings first
                query_lower = query.lower()
                if query_lower in greeting_responses:
                    response = greeting_responses[query_lower]
                else:
                    # Check if the query contains any keywords from our topic responses
                    response = "I don't have specific information on that topic yet. Please try asking about Python learning, study tips, or math help."
                    for key, value in ai_responses.items():
                        if key in query_lower:
                            response = value
                            break
                
                # Add to chat history
                chat_entry = {
                    'query': query, 
                    'response': response,
                    'timestamp': timezone.now().strftime("%H:%M")
                }
                chat_history.append(chat_entry)
                
                # Store updated history in session
                request.session['chat_history'] = chat_history
                context['chat_history'] = chat_history
                
            except Exception as e:
                context['error'] = f"Sorry, I encountered an error: {str(e)}"
    
    return render(request, 'learning_paths/ai_assistant.html', context)