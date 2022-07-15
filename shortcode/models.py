from django.conf import settings
from django.db import models
from django.utils import timezone
from solo.models import SingletonModel

NULL_AND_BLANK = {"null": True, "blank": True}


class ShortCode(models.Model):
    shortcode = models.CharField(
        max_length=settings.SHORTCODE_MAX_LENGTH,
        unique=True,
        verbose_name="Short URL",
        help_text="lowercase short url. Automatically allocated shortcodes are exactly 6-length. User subitted shortcodes are at leat 4-length.",
    )

    original_url = models.CharField(
        max_length=255,
        editable=True,
        verbose_name="Original URL",
        help_text="Original long URL",
    )

    accessed_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="Accessed Count",
        help_text="How many times this short code is accessed",
    )

    last_accessed_at = models.DateTimeField(
        editable=False,
        **NULL_AND_BLANK,
        verbose_name="Last Accessed",
        help_text="Timestamp when the shortcode was last accessed"
    )

    registered_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="Registered",
        help_text="Timestamp when the record was created. The date and time are displayed in the Timezone from where request is made. e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Updated",
        **NULL_AND_BLANK,
        help_text="Timestamp when the record was modified. The date and time are displayed in the Timezone from where request is made. e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC"
    )

    class Meta:
        verbose_name = "ShortCode"
        verbose_name_plural = "ShortCodes"
