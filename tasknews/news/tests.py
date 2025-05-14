# Django
import json
from django.urls import reverse, resolve

# Libraries
from rest_framework.test import APITestCase
from rest_framework import status

# My Apps
from news.models import News, Tags
from .views import NewsList


class TestNewsAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tag1 = Tags.objects.create(name="سیاسی")
        cls.tag2 = Tags.objects.create(name="ورزشی")
        cls.tag3 = Tags.objects.create(name="اقتصادی")

        cls.news1 = News.objects.create(
            title="تحریم جدید", content="سیاست خارجی جدید", source="تسنیم"
        )
        cls.news1.tags.add(cls.tag1)

        cls.news2 = News.objects.create(
            title="قهرمانی ایران", content="جام جهانی فوتبال", source="تسنیم"
        )
        cls.news2.tags.add(cls.tag2)

        cls.news3 = News.objects.create(
            title="ریزش بورس", content="اقتصاد کشور دچار بحران شد", source="تسنیم"
        )
        cls.news3.tags.add(cls.tag3)

        cls.news4 = News.objects.create(
            title="باخت ایران", content="جام جهانی ادامه دارد", source="تسنیم"
        )
        cls.news4.tags.add(cls.tag2, cls.tag3)

    def test_news_list_url_exists(self):
        url = reverse("news-list")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, NewsList)
        self.assertEqual(resolver.view_name, "news-list")

    def test_url_root(self):
        url = reverse("news-list")
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))

    def test_filter_by_tags(self):
        url = reverse("news-list")
        response = self.client.get(url, {"tags": "ورزشی اقتصادی"})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 3)
        titles = [item["title"] for item in response_data]
        self.assertIn("باخت ایران", titles)

    def test_filter_by_keyword(self):
        url = reverse("news-list")
        response = self.client.get(url, {"search": "جهانی ایران"})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)
        titles = [item["title"] for item in response_data]
        self.assertIn("قهرمانی ایران", titles)

    def test_filter_by_exclude(self):
        url = reverse("news-list")
        response = self.client.get(url, {"exclude": "بورس"})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        titles = [item["title"] for item in response_data]
        self.assertNotIn("ریزش بورس", titles)

    def test_filter_by_tags_and_keyword(self):
        url = reverse("news-list")
        response = self.client.get(url, {"tags": "ورزشی", "search": "ایران"})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)
        titles = [item["title"] for item in response_data]
        self.assertNotIn("ریزش بورس", titles)
