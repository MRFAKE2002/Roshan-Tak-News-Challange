# Libraries
from rest_framework import generics

# My Apps
from .models import News
from .serializers import NewsSerializers


# ---------------------------------------< News List >----------------------------------- #


class NewsList(generics.ListAPIView):
    queryset = News.objects.prefetch_related("tags").all().order_by("-created_at")
    serializer_class = NewsSerializers
