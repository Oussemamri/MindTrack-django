from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import StudySession, StudyActivity
from .forms import StudySessionForm, StudyActivityForm

@login_required
def session_list(request):
    sessions = StudySession.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'study_sessions/session_list.html', {
        'sessions': sessions
    })

@login_required
def session_create(request):
    if request.method == 'POST':
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.status = 'in_progress'
            session.save()
            form.save_m2m()  # Save topics
            messages.success(request, 'Study session created successfully!')
            return redirect('study_sessions:session_detail', pk=session.pk)
    else:
        form = StudySessionForm()
    return render(request, 'study_sessions/session_form.html', {'form': form})

@login_required
def session_detail(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    activities = session.activities.all().order_by('-start_time')
    activity_form = StudyActivityForm() if session.status == 'in_progress' else None
    
    return render(request, 'study_sessions/session_detail.html', {
        'session': session,
        'activities': activities,
        'activity_form': activity_form
    })

@login_required
def session_update(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StudySessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Study session updated successfully!')
            return redirect('study_sessions:session_detail', pk=session.pk)
    else:
        form = StudySessionForm(instance=session)
    return render(request, 'study_sessions/session_form.html', {
        'form': form,
        'session': session
    })

@login_required
def session_delete(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'Study session deleted successfully!')
        return redirect('study_sessions:session_list')
    return render(request, 'study_sessions/session_confirm_delete.html', {
        'session': session
    })

@login_required
def add_activity(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    if request.method == 'POST' and session.status == 'in_progress':
        form = StudyActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.session = session
            activity.save()
            messages.success(request, 'Activity added successfully!')
    return redirect('study_sessions:session_detail', pk=pk)

@login_required
def complete_session(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    session.status = 'completed'
    session.end_time = timezone.now()
    session.save()
    messages.success(request, 'Session completed successfully!')
    return redirect('study_sessions:session_list')

@login_required
def pause_session(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    session.status = 'paused'
    session.save()
    messages.success(request, 'Session paused successfully!')
    return redirect('study_sessions:session_list')

@login_required
def resume_session(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    session.status = 'in_progress'
    session.save()
    messages.success(request, 'Session resumed successfully!')
    return redirect('study_sessions:session_detail', pk=pk)
