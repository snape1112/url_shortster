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
    },
]


class SubmitTest(APITestCase):
    submit_url = "/submit"

    def test_shortcode(self):
        response = self.client.post(self.submit_url, SampleData[0], format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["shortcode"], SampleData[0]["shortcode"].lower())

    def test_default_shortcode(self):
        data = {
            "original_url": SampleData[0]["original_url"],
        }
        response = self.client.post(self.submit_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        shortcode = response.data["shortcode"]
        self.assertNotEqual(re.match("^[a-z0-9]{6}$", shortcode), None)

    def test_invalid_length(self):
        data = {
            "original_url": SampleData[0]["original_url"],
            "shortcode": "go",
        }

        response = self.client.post(self.submit_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_shortcode(self):
        data = {
            "original_url": SampleData[0]["original_url"],
            "shortcode": "goo_gle",
        }

        response = self.client.post(self.submit_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique(self):
        self.client.post(self.submit_url, SampleData[0], format="json")

        data = {
            "original_url": SampleData[1]["original_url"],
            "shortcode": SampleData[0]["shortcode"],
        }

        response = self.client.post(self.submit_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_case_insensitive(self):
        self.client.post(self.submit_url, SampleData[0], format="json")

        data = {
            "original_url": SampleData[1]["original_url"],
            "shortcode": SampleData[0]["shortcode"].upper(),
        }

        response = self.client.post(self.submit_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RedirectTest(APITestCase):
    submit_url = "/submit"

    def setUp(self):
        self.client.post(self.submit_url, SampleData[0], format="json")
        self.client.post(self.submit_url, SampleData[1], format="json")

    def test_redirect(self):
        response = self.client.get("/" + SampleData[0]["shortcode"])

        self.assertRedirects(
            response, SampleData[0]["original_url"], target_status_code=302
        )

    def test_invalid(self):
        response = self.client.get("/medium")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_case_insensitive(self):
        response = self.client.get("/" + SampleData[0]["shortcode"].upper())

        self.assertRedirects(
            response, SampleData[0]["original_url"], target_status_code=302
        )


class RetrieveStatsTest(APITestCase):
    submit_url = "/submit"
    stats_url = "/stats"

    def setUp(self):
        self.client.post(self.submit_url, SampleData[0], format="json")
        for _ in range(3):
            self.client.get("/" + SampleData[0]["shortcode"])

    def test_stats(self):
        response = self.client.get("/" + SampleData[0]["shortcode"] + "/stats")

        self.assertEqual(response.data["accessed_count"], 3)

    def test_invalid(self):
        response = self.client.get("/medium")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_case_insensitive(self):
        response = self.client.get("/" + SampleData[0]["shortcode"] + "/stats")

        self.assertEqual(response.data["accessed_count"], 3)


class UpdateTest(APITestCase):
    submit_url = "/submit"

    def setUp(self):
        self.client.post(self.submit_url, SampleData[0], format="json")

    def test_patch_url(self):
        data = {
            "original_url": SampleData[1]["original_url"],
        }
        response = self.client.patch(
            "/" + SampleData[0]["shortcode"], data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        code = ShortCode.objects.get(shortcode=SampleData[0]["shortcode"])
        self.assertEqual(code.original_url, SampleData[1]["original_url"])

    def test_patch_shortcode(self):
        data = {
            "shortcode": SampleData[1]["shortcode"],
        }
        response = self.client.patch(
            "/" + SampleData[0]["shortcode"], data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            ShortCode.objects.filter(shortcode=SampleData[0]["shortcode"]).first(), None
        )
        self.assertNotEqual(
            ShortCode.objects.filter(shortcode=SampleData[1]["shortcode"]).first(), None
        )

    def test_invalid_shortcode(self):
        data = {
            "shortcode": "goo_gle",
        }
        response = self.client.patch(
            "/" + SampleData[0]["shortcode"], data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid(self):
        data = {
            "shortcode": SampleData[1]["shortcode"],
        }
        response = self.client.patch("/medium", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteTest(APITestCase):
    submit_url = "/submit"

    def setUp(self):
        self.client.post(self.submit_url, SampleData[0], format="json")

    def test_delete(self):
        response = self.client.delete(
            "/" + SampleData[0]["shortcode"], {}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            ShortCode.objects.filter(shortcode=SampleData[0]["shortcode"]).first(), None
        )

    def test_invalid(self):
        response = self.client.delete("/medium")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
