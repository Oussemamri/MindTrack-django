from django.db import models
from django.conf import settings
from quiz_app.models import Topic, Quiz

class LearningPath(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_paths')
    topics = models.ManyToManyField(Topic, through='PathTopic')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class PathTopic(models.Model):
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    required_quizzes = models.ManyToManyField(Quiz, blank=True)
    completion_threshold = models.PositiveIntegerField(default=70)

    class Meta:
        ordering = ['order']
        unique_together = ['path', 'order']

    def is_completed_by_user(self, user):
        if not self.required_quizzes.exists():
            return True
        
        for quiz in self.required_quizzes.all():
            best_attempt = quiz.attempts.filter(
                user=user
            ).order_by('-score').first()
            
            if not best_attempt or best_attempt.score < self.completion_threshold:
                return False
        return True

class PathEnrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE)
    current_topic = models.ForeignKey(PathTopic, on_delete=models.SET_NULL, null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'path']

    @property
    def completion_percentage(self):
        total_topics = self.path.pathtopic_set.count()
        if total_topics == 0:
            return 0
            
        completed_topics = sum(
            1 for topic in self.path.pathtopic_set.all() 
            if topic.is_completed_by_user(self.user)
        )
        return int((completed_topics / total_topics) * 100)