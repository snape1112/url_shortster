import zlib
import string

from .models import ShortCode


def generate_shortcode(url):
    allowed_chars = "".join((string.ascii_lowercase, string.digits))
    allowed_length = len(allowed_chars)
    suffix = 0
    while True:
        _str = url + (str(suffix) if suffix else "")
        hash = zlib.crc32(_str.encode("utf-8"))
        unique_code = ""
        for i in range(6):
            unique_code += allowed_chars[hash % allowed_length]
            hash = int(hash / allowed_length)
        if not ShortCode.objects.filter(shortcode=unique_code).first():
            return unique_code
        else:
            suffix += 1