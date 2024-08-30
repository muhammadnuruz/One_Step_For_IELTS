from rest_framework import serializers

from apps.audios.models import Audios


class AudiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audios
        fields = "__all__"
