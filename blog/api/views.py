import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import BlogPost
from ..utils import fetchByTags


class PingResponse(APIView):
    """
    Just Ping api
    """

    def get(self, request, *args, **kwargs):
        response = {
            "success": True,
        }
        return Response(response)


class PostsResponse(APIView):
    """
    Fetch posts from hatchways by given tags and return the list by given sortby and direction
    Args:
        tags (str, required): tags joined by comma ex: "tech, design"
        sortBy (str, optional): sort field. default is "id". Possible values are id, reads, likes, popularity
        direction (str, optional): direction of sort. default is "asc". Possible values are asc and desc.
    """

    def register_error(self, msg):
        data = {"error": msg}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # check if tags is not empty
        tags = request.GET.get("tags", None)
        if not tags:
            return self.register_error("Tags parameter is required")

        # check sortBy is valid
        sortBy = request.GET.get("sortBy", "id")
        if sortBy not in ["id", "reads", "likes", "popularity"]:
            return self.register_error("sortBy parameter is invalid")

        # check direction is valid
        direction = request.GET.get("direction", "asc")
        if direction not in ["asc", "desc"]:
            return self.register_error("direction parameter is invalid")

        # split tags string into array and fetch posts
        tags = tags.split(", ")
        fetchByTags(tags)

        # filter posts by tags to get result
        result = None
        for tag in tags:
            queryset = BlogPost.objects.filter(tags__contains=tag)
            result = result.union(queryset) if result else queryset
        sortBy = sortBy if direction == "asc" else f"-{sortBy}"
        result = result.order_by(sortBy).values() if result else []

        data = {"posts": result, "count": len(result)}
        return Response(data)
