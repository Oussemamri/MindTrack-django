from django.db import models
from django.conf import settings

class Topic(models.Model):
    CATEGORY_CHOICES = [
        ('linux', 'Linux'),
        ('devops', 'DevOps'),
        ('docker', 'Docker'),
        ('code', 'Programming'),
        ('sql', 'SQL'),
        ('cms', 'CMS'),
        ('math', 'Mathematics'),
        ('history', 'History'),
        ('science', 'Science'),
        ('geography', 'Geography'),
        ('literature', 'Literature'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
    ]
    
    name = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower()
        super().save(*args, **kwargs)

class Quiz(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions", null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"Submission by {username} for {self.quiz.title}"

class SubmissionAnswer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="submission_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Answer by {self.submission.user.username} for {self.question.text}"
