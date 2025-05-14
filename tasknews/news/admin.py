# Django
from django.contrib import admin

# My Apps
from .models import News, Tags


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

    list_per_page = 10

    search_fields = ["name"]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "content",
        "source",
        "get_tags",
        "get_tags_count",
        "created_at",
    ]

    list_per_page = 10

    list_filter = ["tags"]

    search_fields = ["title", "content"]

    def get_tags(self, obj):
        """
        Show name of tags in each news
        """
        return ", ".join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = "Tags"

    def get_tags_count(self, obj):
        """
        Get count of tags in each news
        """
        return obj.tags.count()

    get_tags_count.short_description = "# Tags"
