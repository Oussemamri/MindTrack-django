from django import forms
from .models import StudySession, StudyActivity
from quiz_app.models import Topic

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['title', 'description', 'topics']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'topics': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show the five technical topics
        self.fields['topics'].queryset = Topic.objects.filter(
            name__in=['linux', 'devops', 'docker', 'code', 'sql']
        )

class StudyActivityForm(forms.ModelForm):
    class Meta:
        model = StudyActivity
        fields = ['activity_type', 'notes', 'duration']
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }