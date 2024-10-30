from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    @property
    def is_teacher(self):
        return self.role == 'teacher'
    
    @property
    def is_student(self):
        return self.role == 'student'

    class Meta:
        db_table = 'auth_user'
        app_label = 'accounts'
