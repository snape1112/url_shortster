from msilib.schema import Shortcut
import random
import string

from .models import ShortCode, ShortCodeSetting


def generate_shortcode():
    setting = ShortCodeSetting.get_solo()
    index = setting.generated_count + 1
    allowed_chars = "".join((string.ascii_lowercase, string.digits))
    while True:
        unique_id = "".join(random.choice(allowed_chars) for _ in range(6))
        if not ShortCode.objects.filter(shortcode=unique_id).first():
            setting.generated_count = index
            return unique_id
        index += 1
