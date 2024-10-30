from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Quiz, Question, Answer, Submission
from .forms import QuizGenerationForm, QuizSubmissionForm
from .ai_utils import QuestionGenerator, RateLimitExceeded

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

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        form = QuizSubmissionForm(request.POST, quiz=quiz)
        if form.is_valid():
            score = calculate_score(form, quiz)
            # Create submission without user for now
            submission = Submission.objects.create(
                quiz=quiz,
                score=score
            )
            return redirect('quiz_app:quiz_results', submission_id=submission.id)
    else:
        form = QuizSubmissionForm(quiz=quiz)
    
    return render(request, 'quiz_app/take_quiz.html', {'quiz': quiz, 'form': form})

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
