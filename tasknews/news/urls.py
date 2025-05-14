# Django
from django.urls import path

# My Apps
from . import views

urlpatterns = [
    #! News | List
    path("news/", views.NewsList.as_view(), name="news-list"),
]
