from rest_framework import serializers
from keywords.models import Keyword, VideoItem


class KeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keyword
        fields = ('id', 'name')


class VideoItemSerializer(serializers.ModelSerializer):

    link = serializers.CharField(source='get_link')

    class Meta:
        model = VideoItem
        exclude = ('keywords', 'created_at', 'updated_at')
