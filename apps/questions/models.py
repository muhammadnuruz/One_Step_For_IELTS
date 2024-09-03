from django.db import models

from apps.audios.models import Audios


class Questions(models.Model):
    TYPE_CHOICES = [
        ('multiple choice', "Multiple Choice"),
        ('matching', "Matching"),
        ('plan, map, diagram labeling', "Plan, Map, Diagram Labeling"),
        ('form, note, table, flow-chart, summary completion', "Form, Note, Table, Flow-chart, Summary Completion"),
        ('sentence completion', "Sentence Completion"),
        ('short answer questions', "Short Answer Questions"),
        ('pick from a list', "Pick from a list"),
    ]
    audio = models.ForeignKey(Audios, related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    question_number = models.IntegerField()
    condition = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    options = models.JSONField(default=dict, blank=True, null=True)
    correct_answer = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Question"
