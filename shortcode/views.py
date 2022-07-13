from django.shortcuts import render

class ShortCodeViewSet(
    LoggingMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
    ListModelMixin,
):