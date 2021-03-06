from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics

from keywords.filters import VideoItemFilter
from keywords.models import Keyword, VideoItem
from keywords.serializers import KeywordSerializer, VideoItemSerializer


class KeywordViewSet(viewsets.ModelViewSet):
    """ API for retrieve, update, remove keywords for requested user """

    serializer_class = KeywordSerializer

    def get_queryset(self):
        return Keyword.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoItemListView(generics.ListAPIView):
    """
    API for retrieving list of videos by requested keyword-id.
    It can be filtered by date
    and paginated by settings.REST_FRAMEWORK['PAGE_SIZE'] value
    """

    serializer_class = VideoItemSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VideoItemFilter

    def get_queryset(self):
        return VideoItem.objects.filter(keywords__id=self.kwargs['keyword_id'])
