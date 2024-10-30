from django import forms
from .models import StudySession, StudyActivity

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['title', 'description', 'topics']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'topics': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

class StudyActivityForm(forms.ModelForm):
    class Meta:
        model = StudyActivity
        fields = ['activity_type', 'quiz', 'notes']
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'quiz': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        } 