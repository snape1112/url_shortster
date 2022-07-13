from msvcrt import getwch
from django.urls import path, reverse, include, resolve
from django.test import SimpleTestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .api.views import PingResponse, PostsResponse
import random

class ApiUrlsTests(SimpleTestCase):
    def test_ping_is_resolved(self):
        url = reverse('ping')
        self.assertEquals(resolve(url).func.view_class, PingResponse)

    def test_posts_is_resolved(self):
        url = reverse('posts')
        self.assertEquals(resolve(url).func.view_class, PostsResponse)
        
class PingTest(APITestCase):
    ping_url = reverse('ping')
    
    def test(self):
        response = self.client.get(self.ping_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()
        self.assertEqual(response["success"], True)

class PostsTest(APITestCase):
    post_url = reverse('posts')

    def test_empty_tags(self):
        response = self.client.get(self.post_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = response.json()
        self.assertEqual(response["error"], "Tags parameter is required")

    def test_invalid_sortBy(self):
        data = {
            "tags": "tech",
            "sortBy": "author",
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = response.json()
        self.assertEqual(response["error"], "sortBy parameter is invalid")

    def test_invalid_sortBy(self):
        data = {
            "tags": "tech",
            "direction": "increase",
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = response.json()
        self.assertEqual(response["error"], "direction parameter is invalid")

    def test_one_tag(self):
        data = {
            "tags": "tech"
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()
        posts = response["posts"]
        self.assertEqual(len(posts), response["count"])

    def test_more_tags(self):
        data = {
            "tags": "tech, culture, health"
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()
        posts = response["posts"]
        self.assertEqual(len(posts), response["count"])

    def test_direction_default_asc(self):
        data = {
            "tags": "tech"
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()
        posts = response["posts"]
        self.assertEqual(len(posts), response["count"])
        index = random.randint(1, len(posts) - 1)
        self.assertLess(int(posts[0]["id"]), int(posts[index]["id"]))

    def test_direction_desc(self):
        data = {
            "tags": "tech",
            "direction": "desc",
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()
        posts = response["posts"]
        self.assertEqual(len(posts), response["count"])
        index = random.randint(1, len(posts) - 1)
        self.assertGreater(int(posts[0]["id"]), int(posts[index]["id"]))

    def test_sortBy_id(self):
        data = {
            "tags": "tech",
            "sortBy": "id",
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()
        posts = response["posts"]
        self.assertEqual(len(posts), response["count"])
        index = random.randint(1, len(posts) - 1)
        self.assertLess(int(posts[0]["id"]), int(posts[index]["id"]))

    def test_sortBy_reads(self):
        data = {
            "tags": "tech",
            "sortBy": "reads",
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()
        posts = response["posts"]
        self.assertEqual(len(posts), response["count"])
        index = random.randint(1, len(posts) - 1)
        self.assertLess(int(posts[0]["reads"]), int(posts[index]["reads"]))

    def test_sortBy_likes(self):
        data = {
            "tags": "tech",
            "sortBy": "likes",
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()
        posts = response["posts"]
        self.assertEqual(len(posts), response["count"])
        index = random.randint(1, len(posts) - 1)
        self.assertLess(int(posts[0]["likes"]), int(posts[index]["likes"]))

    def test_sortBy_popularity(self):
        data = {
            "tags": "tech",
            "sortBy": "likes",
        }
        response = self.client.get(self.post_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()
        posts = response["posts"]
        self.assertEqual(len(posts), response["count"])
        index = random.randint(1, len(posts) - 1)
        self.assertLess(float(posts[0]["popularity"]), float(posts[index]["popularity"]))
