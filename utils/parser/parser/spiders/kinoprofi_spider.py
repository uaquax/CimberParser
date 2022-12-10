from random_user_agent.user_agent import UserAgent
from tqdm import tqdm
from bs4 import BeautifulSoup, Comment
from selectolax.parser import HTMLParser

import scrapy
import httpx

from models.Website import Website


class KinoprofiSpider(scrapy.Spider):
    name = "kinoprofi"
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
            yield scrapy.Request(Website.Kinoprofi.value.format(i))


    def get_total_pages(self):
        resp = httpx.get("https://kinoprofi.vip/",
                         headers=self.headers)
        html = HTMLParser(resp.text)

        return int(html.css_first("div.navigation").css("a")[-2].text().strip())


    def parse(self, response, **kwargs):
        for i in response.css("div.sh-block.ns"):
            link = i.css("a[itemprop='url']").xpath("@href").get()

            yield scrapy.Request(link, self.parse_film)

    def parse_film(self, response):
        name = response.css("h1[itemprop='name']").xpath("text()").get().split("(")[0].strip()

        info_list = response.css("div.more-info")
        year = info_list[1].css("i").xpath("text()").get()
        duration = response.css("span.offset").xpath("text()").get()
        poster = response.css("img[itemprop='image']").xpath("@src").get()
        players = [i.xpath("@src").get().strip() for i in response.css("iframe")]
        countries = [i.xpath("text()").get().strip() for i in response.css("span.country")]
        genres = [i.css("a").xpath("text()").get().split() for i in response.css("span[itemprop='genre']")]

        soup = BeautifulSoup(response.body, "lxml")
        description = soup.find("div", itemprop="description").get_text(separator="\n", strip=True)

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
