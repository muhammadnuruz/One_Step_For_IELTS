from django.contrib import admin

from apps.questions.models import Questions
from apps.audios.models import Audios


class QuestionsInline(admin.TabularInline):
    model = Questions
    extra = 0


class AudiosAdmin(admin.ModelAdmin):
    list_display = ('section', 'type', 'audio_file', 'created_at')
    list_filter = ('section', 'type')
    inlines = [QuestionsInline]


admin.site.register(Audios, AudiosAdmin)
