from django import forms
from django.forms import inlineformset_factory
from .models import LearningPath, PathTopic
from quiz_app.models import Topic, Quiz

class LearningPathForm(forms.ModelForm):
    class Meta:
        model = LearningPath
        fields = ['title', 'description', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class PathTopicForm(forms.ModelForm):
    required_quizzes = forms.ModelMultipleChoiceField(
        queryset=Quiz.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'quiz-checkbox-list'})
    )

    completion_threshold = forms.IntegerField(
        initial=80,  # Default value of 80%
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'topic_id') and self.instance.topic_id:
            self.fields['required_quizzes'].queryset = Quiz.objects.filter(topic=self.instance.topic)
        else:
            self.fields['required_quizzes'].queryset = Quiz.objects.all()

        self.fields['topic'].widget.attrs.update({'class': 'form-select'})
        self.fields['topic'].widget.attrs.update({
            'onchange': 'updateQuizzes(this)'
        })

    class Meta:
        model = PathTopic
        fields = ['topic', 'order', 'required_quizzes', 'completion_threshold']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

PathTopicFormSet = inlineformset_factory(
    LearningPath,
    PathTopic,
    form=PathTopicForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
    validate_max=True,
    max_num=10  # Limit maximum number of topics
)