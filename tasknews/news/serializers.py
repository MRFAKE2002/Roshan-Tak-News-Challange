# Libraries
from rest_framework.serializers import ModelSerializer

# My Apps
from .models import News, Tags


class TagsSerializers(ModelSerializer):

    class Meta:
        model = Tags
        fields = ["id", "name"]


class NewsSerializers(ModelSerializer):
    tags = TagsSerializers(many=True, read_only=True)

    class Meta:
        model = News
        fields = ["id", "title", "content", "source", "tags", "created_at"]
