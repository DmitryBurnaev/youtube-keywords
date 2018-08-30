from rest_framework import serializers
from keywords.models import Keyword, VideoItem


class KeywordSerializer(serializers.ModelSerializer):
    """ Simple representation keyword data for retrieve or modify API """

    class Meta:
        model = Keyword
        fields = ('id', 'name')


class VideoItemSerializer(serializers.ModelSerializer):
    """ Representation video item for retrieve that via API """

    link = serializers.CharField(source='get_link')

    class Meta:
        model = VideoItem
        exclude = ('keywords', 'created_at', 'updated_at')
