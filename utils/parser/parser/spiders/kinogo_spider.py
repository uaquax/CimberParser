from random_user_agent.user_agent import UserAgent
from tqdm import tqdm
from bs4 import BeautifulSoup, Comment
from selectolax.parser import HTMLParser

import scrapy
import httpx

from models.Website import Website


class KinogoSpider(scrapy.Spider):
    name = "kinogo"
    custom_settings = {
        "FEEDS": {
            "cimber_temp.json": {
                "format": "json",
                "overwrite": True
            }
        },
        "FEED_EXPORT_ENCODING": "utf-8"
    }
    user_agent = UserAgent().get_random_user_agent()
    headers = {'User-Agent': user_agent}



    def start_requests(self):
        total_pages = self.get_total_pages()

        for i in tqdm(range(1, total_pages)):
            yield scrapy.Request(Website.Kinogo.value.format(i))


    def get_total_pages(self):
        resp = httpx.get("https://kinogo-net.la",
                         headers=self.headers)
        html = HTMLParser(resp.text)

        return int(html.css_first("span.navigation").css("a")[-1].text().strip())


    def parse(self, response, **kwargs):
        for i in response.css("div.kino-item.ignore-select.kino-fix"):
            link = i.css("a.kino-h").xpath("@href").get()

            yield scrapy.Request(link, self.parse_film)

    def parse_film(self, response):
        name = response.css("h1.kino-h").xpath("text()").get().strip()

        info_list = response.css("div.kino-lines.ignore-select").css("ul")
        year = info_list.css("li")[0].xpath("text()").get()
        duration = ""
        poster = f"""https://kinogo-net.la{response.css("img[itemprop='image']").xpath("@src").get()}"""
        players = [i.xpath("@src").get().strip() for i in response.css("iframe")]

        yield {
            "name": name,
            "poster": poster,
            "duration": duration,
            "countries": countries,
            "year": year,
            "description": description.strip(),
            "genres": genres,
            "players": players
        }
