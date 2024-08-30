from django.db import models


class Words(models.Model):
    LEVEL_CHOICES = [
        ('a1', "A1"),
        ('a2', "A2"),
        ('b1', "B1"),
        ('b2', "B2"),
        ('c1', "C1"),
        ('c2', "C2"),
    ]
    word = models.CharField(max_length=255)
    definition = models.CharField(max_length=255)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"

    def __str__(self):
        return f"{self.word} - {self.level}"
