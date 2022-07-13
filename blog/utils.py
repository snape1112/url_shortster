import asyncio
import json

import aiohttp
import requests
from django.conf import settings

from .models import BlogPost, TagHistory


async def fetchBlogs(tag, session):
    """
    Fetch blog posts from hatchways blog post url
    """
    url = f"{settings.HATCHWAYS_BLOG_URL}?tag={tag}"
    response = await session.request("GET", url=url)
    response = await response.json()
    return response["posts"]


async def concurrentFetch(tags):
    """
    Run fetch as concurrent
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetchBlogs(tag, session) for tag in tags]
        result = await asyncio.gather(*tasks, return_exceptions=True)
    return result


def fetchByTags(tags):
    """
    Fetch posts by tags and save them into db
    """
    # filter already fetched tags
    fetch_tags = []
    for tag in tags:
        if not TagHistory.objects.filter(name=tag).exists():
            fetch_tags.append(tag)
            TagHistory.objects.create(name=tag)

    # fetch posts
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    posts_list = asyncio.run(concurrentFetch(fetch_tags))

    # save them into db
    for posts in posts_list:
        for post in posts:
            BlogPost.objects.update_or_create(id=post["id"], defaults=post)
