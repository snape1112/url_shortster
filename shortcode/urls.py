from django.urls import path

from .views import ShortCodeCreateView, ShortCodeStatsResponse, ShortCodeViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('/submit', ShortCodeCreateView.as_view(), name="submit"),
    path('/<shortcode>/stats', ShortCodeStatsResponse.as_view(), name="stats")
]

router.register('/', ShortCodeViewSet)