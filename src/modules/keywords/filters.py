from django_filters import rest_framework as filters

from keywords.models import VideoItem


class VideoItemFilter(filters.FilterSet):
    date__gte = filters.DateFilter(field_name="published_at", lookup_expr='gte')
    date__lte = filters.DateFilter(field_name="published_at", lookup_expr='lte')

    class Meta:
        model = VideoItem
        fields = ('published_at',)
