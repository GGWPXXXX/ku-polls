from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    """
    Inline class for displaying choices when editing a question in the admin panel.
    """
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Question model.
    """
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Set publish date", {"fields": ["pub_date"], "classes": ["collapse"]}),
        ("Set end date", {"fields": ["end_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently", "end_date"]
    list_filter = ["pub_date"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
