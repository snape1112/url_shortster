from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import re
from .models import ShortCode
from django.conf import settings

class ShortCodeSerializer(serializers.Serializer):
    shortcode = serializers.CharField(
        max_length=settings.SHORTCODE_MAX_LENGTH,
        required=False,
        help_text="Short URL. Automatically allocated shortcodes are exactly 6-length. User subitted shortcodes are at leat 4-length.",
    )

    def validate_shortcode(self, value):
        # user submitted code must be at least 4 characters long
        if value:
            if len(value) < 4:
                raise ValidationError("Submitted shortcode must be at leat 4 characters long.")
            value = value.lower()
            if not re.match("[0-9|a-z]", value):
                raise ValidationError("Submitted shortcode can contain digits, upper case letters, and lowercase letters.")


    class Meta:
        model = ShortCode
        fields = ("shortcode", "original_url")


class ShortCodeStatsSerializer(serializers.Serializer):
    class Meta:
        model = ShortCode
        fields = ("registerd_at", "last_accessed_at", "accessed_count")