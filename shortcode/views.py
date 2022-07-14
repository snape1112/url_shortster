from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import generics
from rest_framework.mixins import (DestroyModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import ShortCode
from .serializers import ShortCodeSerializer, ShortCodeStatsSerializer


class ShortCodeCreateView(generics.CreateAPIView):
    """
    Create Shortcode

    A user can submit a URL to /submit without a shortcode proposed, and receive automatically allocated unique shortcode in response.
    A user can submit a URL to /submit with the desired shortcode and will receive the chosen shortcode if it is available.
    All shortcodes can contain digits, upper case letters, and lowercase letters. It is case in-sensitive.
    Automatically allocated shortcodes are exactly 6 characters long.
    User submitted shortcodes must be at least 4 characters long.
    """

    serializer_class = ShortCodeSerializer
    queryset = ShortCode.objects.all()


class ShortCodeViewSet(
    UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = ShortCodeSerializer
    queryset = ShortCode.objects.all()
    lookup_field = "shortcode"

    def get_object(self):
        shortcode = self.kwargs["shortcode"].lower()
        return get_object_or_404(ShortCode, shortcode=shortcode)

    def retrieve(self, request, *args, **kwargs):
        """
        Redirect Shortcode

        A user can access a /<shortcode> endpoint and be redirected to the URL associated with that shortcode, if it exists.
        """
        code = self.get_object()

        code.accessed_count = code.accessed_count + 1
        code.last_accessed_at = timezone.now()
        code.save()

        return redirect(code.original_url)

    def update(self, request, *args, **kwargs):
        """
        Update Shortcode

        Update shortcode and original url
        As a user, sometimes I will want to customize the short URL so that I can recall what URL it is referencing or give it a cool name
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Parital Update Shortcode

        Partial update shortcode or orignal url
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Destroy Shortcode

        Destroy Shortcode
        """
        return super().destroy(request, *args, **kwargs)


class ShortCodeStatsResponse(generics.GenericAPIView):
    """
    Shortcode Stats

    A user can access a /<shortcode>/stats endpoint in order to see when the shortcode was registered, when it was last accessed, and how many times it was accessed.
    """
    serializer_class = ShortCodeStatsSerializer
    queryset = ShortCode.objects.all()

    def get(self, request, shortcode, *args, **kwargs):
        code = get_object_or_404(ShortCode, shortcode=shortcode.lower())
        serializer = self.get_serializer(code)
        return Response(serializer.data)
