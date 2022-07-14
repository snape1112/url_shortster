import random
import string

from django.apps import apps

def generate_shortcode():
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    while True:
        unique_id = ''.join(random.choice(allowed_chars) for _ in range(6))
        ShortCode = apps.get_model("shortcode.Shortcode")
        if not ShortCode.objects.filter(short_code=unique_id).first():
            return unique_id