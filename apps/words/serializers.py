from rest_framework import serializers

from apps.words.models import Words


class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields = "__all__"


class WordsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        exclude = ['created_at', 'updated_at']
