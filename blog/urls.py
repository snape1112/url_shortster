from django.urls import path, include
from .api.views import PingResponse, PostsResponse

urlpatterns = [
    path('ping', PingResponse.as_view(), name="ping"),
    path('posts', PostsResponse.as_view(), name="posts")
]
