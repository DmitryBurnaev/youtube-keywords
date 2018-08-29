from rest_framework import viewsets

from keywords.models import Keyword
from keywords.serializers import KeywordSerializer


class KeywordViewSet(viewsets.ModelViewSet):
    serializer_class = KeywordSerializer

    def get_queryset(self):
        return Keyword.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
