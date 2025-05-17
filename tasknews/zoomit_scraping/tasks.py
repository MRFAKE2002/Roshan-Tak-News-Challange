# Django
import django

# Libraries
import os
import sys
import pathlib
from celery import shared_task


sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasknews.settings")
django.setup()

# My Apps
from zoomit_scraping.scraper import get_article_links, extract_article_data
from news.models import News, Tags


@shared_task
def get_save_zoomit_articles():
    article_links = get_article_links()
    print(f"There is {len(article_links)} articles here.")
    print("-----------------------------------")

    for i, link in enumerate(article_links[:5], start=1):
        print(f"\n {i}: {link}")

        data = extract_article_data(link)

        if data:
            print(f"title: {data['title']}")
            print(f"tags: {', '.join(data['tags'])}")
            print(
                f"paragraphs: {data['paragraphs'][0] if data['paragraphs'] else 'There is no paragraphs.'}"
            )

            if not News.objects.filter(source=data["url"]).exists():
                news_item = News.objects.create(
                    title=data["title"],
                    content="\n\n".join(data["paragraphs"]),
                    source=data["url"],
                )

                for tag_name in data["tags"]:
                    tag_obj, created = Tags.objects.get_or_create(name=tag_name)
                    news_item.tags.add(tag_obj)

                print("Article saved successfully.")
            else:

                print("Article already exist. Skipping...")

        else:
            print("[!] There is error about article data !!!")


if __name__ == "__main__":
    get_save_zoomit_articles()
