from django.contrib import admin
from .models import Questions

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_number', 'type', 'created_at', 'updated_at')
    list_filter = ('type', 'question_number', 'created_at')
    search_fields = ('question',)

admin.site.register(Questions, QuestionsAdmin)
