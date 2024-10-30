from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Quiz, Question, Answer, Submission, Topic, QuizAttempt
from .forms import QuizGenerationForm, QuizSubmissionForm
from .ai_utils import QuestionGenerator, RateLimitExceeded

class BaseViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context

class QuizListView(BaseViewMixin, ListView):
    model = Quiz
    template_name = 'quiz_app/quiz_list.html'
    context_object_name = 'quizzes'

class TopicDetailView(BaseViewMixin, DetailView):
    model = Topic
    template_name = 'quiz_app/topic_detail.html'
    context_object_name = 'topic'

def create_quiz(request):
    if request.method == 'POST':
        form = QuizGenerationForm(request.POST)
        if form.is_valid():
            try:
                topic = form.cleaned_data['topic']
                title = form.cleaned_data['title']
                num_questions = form.cleaned_data['num_questions']
                
                question_generator = QuestionGenerator()
                try:
                    generated_questions, is_ai_generated = question_generator.generate_questions(
                        topic=topic.name,
                        num_questions=num_questions
                    )
                    
                    quiz = Quiz.objects.create(
                        topic=topic,
                        title=title
                    )
                    
                    for q_text, answers in generated_questions:
                        question = Question.objects.create(
                            quiz=quiz,
                            text=q_text
                        )
                        for ans_text, is_correct in answers:
                            Answer.objects.create(
                                question=question,
                                text=ans_text,
                                is_correct=is_correct
                            )
                    
                    if is_ai_generated:
                        messages.success(request, 'Quiz created successfully with AI-generated questions!')
                    else:
                        messages.warning(request, 'AI generation failed. Quiz created with fallback questions.')
                    
                    return redirect('quiz_app:quiz_detail', quiz_id=quiz.id)
                    
                except ValueError as e:
                    messages.error(request, str(e))
                    return redirect('quiz_app:create_quiz')
                    
            except RateLimitExceeded:
                messages.error(request, 'Rate limit exceeded. Please try again later.')
                return redirect('quiz_app:create_quiz')
    else:
        form = QuizGenerationForm()
    
    return render(request, 'quiz_app/create_quiz.html', {'form': form})

def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz_app/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_app/quiz_detail.html', {'quiz': quiz})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizSubmissionForm(request.POST, quiz=quiz)
        if form.is_valid():
            score = calculate_score(form, quiz)
            
            # Save the quiz attempt
            QuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                score=score
            )
            
            # Get the path_id from query params if it exists
            path_id = request.GET.get('from_path')
            context = {
                'quiz': quiz,
                'score': score,
            }
            if path_id:
                context['from_path'] = path_id
            
            return render(request, 'quiz_app/quiz_results.html', context)
    else:
        form = QuizSubmissionForm(quiz=quiz)
    
    return render(request, 'quiz_app/take_quiz.html', {
        'quiz': quiz,
        'form': form
    })

def calculate_score(form, quiz):
    correct_answers = 0
    total_questions = quiz.questions.count()
    
    for question in quiz.questions.all():
        selected_answer = form.cleaned_data[f'question_{question.id}']
        if selected_answer.is_correct:
            correct_answers += 1
    
    return (correct_answers / total_questions) * 100 if total_questions > 0 else 0

def quiz_results(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    return render(request, 'quiz_app/quiz_results.html', {'submission': submission})

@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizGenerationForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully!')
            return redirect('quiz_app:quiz_detail', quiz_id=quiz.id)
    else:
        form = QuizGenerationForm(instance=quiz)
    return render(request, 'quiz_app/edit_quiz.html', {'form': form, 'quiz': quiz})

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully!')
        return redirect('quiz_app:quiz_list')
    return render(request, 'quiz_app/delete_quiz.html', {'quiz': quiz})

def topic_detail(request, slug):
    # Get topic with prefetched quizzes
    topic = get_object_or_404(Topic.objects.prefetch_related('quiz_set'), slug=slug)
    
    # Add debug print statements
    print(f"Topic: {topic.name}")
    print(f"Quiz count: {topic.quiz_set.count()}")
    print(f"Quizzes: {list(topic.quiz_set.all())}")
    
    context = {
        'topic': topic,
        'quizzes': topic.quiz_set.all()  # Explicitly pass quizzes to template
    }
    return render(request, 'quiz_app/topic_detail.html', context)
