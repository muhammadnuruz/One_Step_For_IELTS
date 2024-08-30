from django.db import models


class Audios(models.Model):
    TYPE_CHOICES = [
        ('practice', "Practice"),
        ('transaction', "Transaction"),
    ]
    section = models.IntegerField()
    audio_file = models.FileField(upload_to='listening_audio/', blank=True, null=True)
    type = models.CharField(max_length=11, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Audio"
        verbose_name_plural = "Audios"

    def __str__(self):
        return f"ID {self.pk} - Section {self.section}"
