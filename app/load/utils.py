import re


def generate_url_slug(string: str) -> str:
    url_slug = string.replace(" ", "-").lower()
    return re.sub(r"[^a-z-]", "", url_slug)
