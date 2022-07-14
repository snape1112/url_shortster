import re
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ShortCode

SampleData = [
    {
        "original_url": "https://www.google.com",
        "shortcode": "google",
    },
    {
        "original_url": "https://www.github.com",
        "shortcode": "github",
    }
]

class SubmitTest(APITestCase):
    submit_url = '/submit'

    def test_shortcode(self):
        response = self.client.post(self.submit_url, SampleData[0], format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["shortcode"], SampleData[0]["shortcode"].lower())

    def test_default_shortcode(self):
        data = {
            "original_url": SampleData[0]["original_url"],
        }
        response = self.client.post(self.submit_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        shortcode = response.data['shortcode']
        self.assertEqual(len(shortcode), 6)
        self.assertEqual(re.match(shortcode, '[a-z|0-9]'), True)
    
    def test_invalid_length(self):
        data = {
            "original_url": SampleData[0]["original_url"],
            "shortcode": "go",
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_shortcode(self):
        data = {
            "original_url": SampleData[0]["original_url"],
            "shortcode": "goo_gle",
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique(self):
        self.client.post(self.submit_url, SampleData[0], format='json')

        data = {
            "original_url": SampleData[1]["original_url"],
            "shortcode": SampleData[0]["shortcode"],
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_case_insensitive(self):
        self.client.post(self.submit_url, SampleData[0], format='json')

        data = {
            "original_url": SampleData[1]["original_url"],
            "shortcode": SampleData[0]["shortcode"].upper(),
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class RedirectTest(APITestCase):
#     submit_url = '/submit'
    
#     def setUp(self):
#         self.client.post(self.submit_url, SampleData[0], format='json')
#         self.client.post(self.submit_url, SampleData[1], format='json')

#     def test_redirect(self):
#         response = self.client.get(SampleData[0]["shortcode"])

#         self.assertRedirects(response, SampleData[0]["original_url"])
        
#     def test_invalid(self):
#         response = self.client.get("medium")

#         self.assertSetEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
#     def test_case_insensitive(self):
#         response = self.client.get(SampleData[0]["shortcode"].upper())

#         self.assertRedirects(response, SampleData[0]["original_url"])


# class RetrieveStatsTest(APITestCase):
#     submit_url = '/submit'
#     stats_url = '/stats'
    
#     def setUp(self):
#         self.client.post(self.submit_url, SampleData[0], format='json')
#         self.client.post(self.submit_url, SampleData[1], format='json')

#     def test_redirect(self):
#         response = self.client.get(SampleData[0]["shortcode"])

#         self.assertRedirects(response, SampleData[0]["original_url"])
        
#     def test_invalid(self):
#         response = self.client.get("medium")

#         self.assertSetEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
#     def test_case_insensitive(self):
#         response = self.client.get(SampleData[0]["shortcode"].upper())

#         self.assertRedirects(response, SampleData[0]["original_url"])