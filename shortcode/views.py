from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .models import ShortCode
from .serializers import ShortCodeSerializer, ShortCodeStatsSerializer
from django.shortcuts import redirect
from rest_framework.response import Response

class ShortCodeCreateView(generics.CreateAPIView):
    """
    Create new shortcode
    """
    serializer_class = ShortCodeSerializer
    queryset = ShortCode.objects.all()


class ShortCodeViewSet(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = ShortCodeSerializer
    queryset = ShortCode.objects.all()
    lookup_field = "shortcode"

    def get_object(self):
        shortcode = self.kwargs["shortcode"].lower()
        return get_object_or_404(ShortCode, shortcode=shortcode)

    def retrieve(self, request, *args, **kwargs):
        """
        A user can access a /<shortcode> endpoint and be redirected to the URL associated with that shortcode, if it exists.
        """
        code = self.get_object()

        code.accessed_count = code.accessed_count + 1
        code.last_accessed_at = timezone.now()
        code.save()

        redirect(code.original_url)
    
    def update(self, request, *args, **kwargs):
        """
        Update shortcode and original url
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial update shortcode or orignal url
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Destroy shortcode
        """
        return super().destroy(request, *args, **kwargs)


class ShortCodeStatsResponse(generics.GenericAPIView):
    """
    A user can access a /<shortcode>/stats endpoint in order to see when the shortcode was registered, when it was last accessed, and how many times it was accessed.
    """
    serializer_class = ShortCodeStatsSerializer
    queryset = ShortCode.objects.all()

    def get(self, shortcode):
        code = get_object_or_404(ShortCode, shortcode=shortcode.lower())
        serializer = self.get_serializer(code)
        return Response(serializer.data)
