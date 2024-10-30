from django.contrib import admin
from .models import Topic, Quiz, Question, Answer, Submission, SubmissionAnswer

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created_at')
    list_filter = ('topic', 'created_at')
    search_fields = ('title',)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text',)
    inlines = [AnswerInline]

admin.site.register(Answer)
admin.site.register(Submission)
admin.site.register(SubmissionAnswer)
