from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from apps.audios.models import Audios
from apps.audios.serializers import AudiosSerializer
from apps.questions.models import Questions
from apps.questions.serializers import QuestionsSerializer


class AudiosDetailViewSet(RetrieveAPIView):
    queryset = Audios.objects.all()
    serializer_class = AudiosSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        questions = Questions.objects.filter(audio=instance).order_by('question_number')
        questions_serializer = QuestionsSerializer(questions, many=True)

        data = {
            'audio': serializer.data,
            'questions': questions_serializer.data
        }
        return Response(data)


class AudiosListViewSet(ListAPIView):
    queryset = Audios.objects.all()
    serializer_class = AudiosSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        section = kwargs.get('section')
        audio_type = kwargs.get('type')
        audios = Audios.objects.filter(section=section, type=audio_type)
        serializer = self.get_serializer(audios, many=True)
        return Response(serializer.data)
