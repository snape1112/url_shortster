from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (ShortCodeCreateView, ShortCodeStatsResponse,
                    ShortCodeViewSet)

router = DefaultRouter(trailing_slash=False)
router.register("", ShortCodeViewSet)

urlpatterns = [
    path("submit", ShortCodeCreateView.as_view()),
    path("<str:shortcode>/stats", ShortCodeStatsResponse.as_view()),
] + router.urls
