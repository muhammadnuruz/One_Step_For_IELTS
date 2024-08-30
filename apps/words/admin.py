from django.contrib import admin

from apps.words.models import Words


class WordsAdmin(admin.ModelAdmin):
    list_display = ('word', 'definition', 'level', 'created_at')
    list_filter = ('level', 'created_at',)
    search_fields = ('word', 'definition')


admin.site.register(Words, WordsAdmin)
