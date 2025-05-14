# Libraries
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

# My Apps
from .models import News
from .serializers import NewsSerializers
from .filters import NewsFilter


# ---------------------------------------< News List >----------------------------------- #


class NewsList(generics.ListAPIView):
    queryset = News.objects.prefetch_related("tags").all().order_by("-created_at")
    serializer_class = NewsSerializers

    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
