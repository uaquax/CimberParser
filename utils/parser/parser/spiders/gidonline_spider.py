from random_user_agent.user_agent import UserAgent
from tqdm import tqdm
from selectolax.parser import HTMLParser

import scrapy
import httpx

from models.Website import Website


class GidonlineSpider(scrapy.Spider):
    name = "gidonline"
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
            yield scrapy.Request(Website.Gidonline.value.format(i))


    def get_total_pages(self):
        resp = httpx.get("https://gidonline.io",
                         headers=self.headers)
        html = HTMLParser(resp.text)

        return int(html.css_first("a.last")
                   .attributes["href"]
                   .split("page/")[1]
                   .replace("/", "")
                   .strip())


    def parse(self, response, **kwargs):
        for i in response.css("a.mainlink"):
            link = i.xpath("@href").get()

            yield scrapy.Request(link, self.parse_film)

    def parse_film(self, response):
        name = response.css("h1[itemprop='name']").xpath("text()").get()
        year = response.css(
            "div[itemprop='dateCreated']").css("a").xpath("text()").get()
        countries = [i.xpath("text()").get() for i in response.css(
            "div[itemprop='countryOfOrigin']").css("a")]
        genres = [i.xpath("text()").get() for i in response.css(
            "div[itemprop='genre']").css("a")]
        duration = response.css("div[itemprop='duration']").xpath("text()").get()
        description = response.css(
            "div[itemprop='description']").css("p").xpath("text()").get()
        poster = f"""https://gidonline.io{response.css("img.t-img").xpath("@src").get()}"""
        players = [i.xpath("@src").get().split(
            "?partner")[0].strip() for i in response.css("iframe")]

        yield {
            "name": name,
            "poster": poster,
            "duration": duration,
            "countries": countries,
            "year": year,
            "description": description,
            "genres": genres,
            "players": players
        }
