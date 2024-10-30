from django.db import models
from django.conf import settings
from quiz_app.models import Topic, Quiz

class StudySession(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('paused', 'Paused')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    topics = models.ManyToManyField(Topic, related_name='study_sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    total_duration = models.DurationField(null=True, blank=True)
    
    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class StudyActivity(models.Model):
    ACTIVITY_TYPES = [
        ('quiz', 'Quiz Attempt'),
        ('note', 'Note Taking'),
        ('review', 'Topic Review'),
        ('break', 'Break Time')
    ]
    
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    quiz = models.ForeignKey(Quiz, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time']
