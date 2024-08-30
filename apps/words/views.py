from jsonschema.benchmarks.unused_registry import instance
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from apps.words.models import Words
from apps.words.serializers import WordsSerializer, WordsCreateSerializer


class WordsDetailViewSet(RetrieveAPIView):
    queryset = Words.objects.all()
    serializer_class = WordsSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        random_words = Words.objects.exclude(id=instance.id).filter(level=instance.level).order_by('?')[:3]
        random_words_names = [word.definition for word in random_words]

        data = {
            'word': serializer.data,
            'random_definitions': random_words_names
        }
        return Response(data)


class WordsListViewSet(ListAPIView):
    queryset = Words.objects.all()
    serializer_class = WordsSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        level = kwargs.get('level')
        words = Words.objects.filter(level=level)
        serializer = self.get_serializer(words, many=True)
        return Response(serializer.data)
