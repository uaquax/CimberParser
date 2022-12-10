import httpx
from selectolax.parser import HTMLParser


class Checker:
    @staticmethod
    def check_support(url: str) -> bool:
        resp = httpx.get(url)
        html = HTMLParser(resp.text)

        if len(html.css_first("iframe")) > 0 or len(html.css_first("video")) > 0:
            return True
        else:
            return False
