import re

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ShortCode
from .utils import generate_shortcode


class ShortCodeSerializer(serializers.ModelSerializer):
    shortcode = serializers.CharField(
        max_length=settings.SHORTCODE_MAX_LENGTH,
        required=False,
        help_text="Short URL. Automatically allocated shortcodes are exactly 6-length. User subitted shortcodes are at leat 4-length.",
    )

    def validate_shortcode(self, value):
        if value:
            value = value.lower()

            if not re.match("^[0-9a-z]{4,}$", value):
                raise ValidationError(
                    "Submitted shortcode must be at least 4 character long and contain only digits, upper case letters, and lowercase letters."
                )

            if not self.instance and ShortCode.objects.filter(shortcode=value).first():
                raise ValidationError("Submitted shortcode must be unique")

        return value

    def create(self, validated_data):
        shortcode = validated_data.get("shortcode", None)
        original_url = validated_data["original_url"]
        if not shortcode:
            shortcode = generate_shortcode(original_url)

        code = ShortCode.objects.create(original_url=original_url, shortcode=shortcode)
        return code

    class Meta:
        model = ShortCode
        fields = ("shortcode", "original_url")


class ShortCodeStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortCode
        fields = ("registered_at", "last_accessed_at", "accessed_count")
