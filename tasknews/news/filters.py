# Django
from django.db.models import Q

# Libraries
from django_filters import rest_framework as filters

# My Apps
from .models import News, Tags


class NewsFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__name",
        to_field_name="name",
        queryset=Tags.objects.all(),
        label="Filter by Tags",
        conjoined=False,
    )
    search = filters.CharFilter(method="filter_by_keyword", label="Filter By Keyword")
    exclude = filters.CharFilter(
        method="filter_exclude", label="Filter By Exclude Keyword"
    )

    class Meta:
        model = News
        fields = ["tags"]

    def filter_by_tags(self, queryset, name, value):
        tags = [tag.strip() for tag in value.split(" ")]
        return queryset.filter(tags__name__in=tags).distinct()

    def filter_by_keyword(self, queryset, name, value):
        keywords = [word.strip() for word in value.split(" ")]
        # ? query = Q()
        # ? for keyword in keywords:
        # ?     query |= Q(title__icontains=keyword) | Q(content__icontains=keyword)
        # ? return queryset.filter(query)
        for keyword in keywords:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )
        return queryset

    def filter_exclude(self, queryset, name, value):
        exclude_keywords = [word.strip() for word in value.split(" ")]
        for keyword in exclude_keywords:
            queryset = queryset.exclude(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )
        return queryset
