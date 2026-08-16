import secrets
import string

from .models import ShortURL


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    while True:
        short_code = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        if not ShortURL.objects.filter(short_code=short_code).exists():
            return short_code