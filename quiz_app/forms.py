from django import forms
from .models import Quiz, Topic, Submission, SubmissionAnswer

class QuizGenerationForm(forms.ModelForm):
    num_questions = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Quiz
        fields = ['topic', 'title']
        widgets = {
            'topic': forms.Select(attrs={
                'class': 'form-select form-control',
                'style': 'border-radius: 10px; padding: 12px;'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }

class QuizSubmissionForm(forms.Form):
    def __init__(self, *args, quiz=None, **kwargs):
        super().__init__(*args, **kwargs)
        if quiz:
            for question in quiz.questions.all():
                self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                    queryset=question.answers.all(),
                    widget=forms.RadioSelect,
                    label=question.text,
                    required=True
                ) 