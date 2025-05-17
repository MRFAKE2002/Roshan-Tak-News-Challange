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
        "short_content",
        "source",
        "get_tags",
        "get_tags_count",
        "created_at",
    ]

    list_per_page = 10

    list_filter = ["tags"]

    search_fields = ["title", "content"]

    def short_content(self, obj):
        """
        Show just 10 words of content.
        """
        words = obj.content.split()
        return " ".join(words[:10]) + ("..." if len(words) > 10 else "")

    short_content.short_description = "Content"

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
