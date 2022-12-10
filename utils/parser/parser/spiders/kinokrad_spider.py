from random_user_agent.user_agent import UserAgent
from tqdm import tqdm
from bs4 import BeautifulSoup, Comment
from selectolax.parser import HTMLParser

import scrapy
import httpx

from models.Website import Website


class KinokradSpider(scrapy.Spider):
    name = "kinokrad"
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
            yield scrapy.Request(Website.Kinokrad.value.format(i))


    def get_total_pages(self):
        resp = httpx.get("https://kinokrad.cc",
                         headers=self.headers)
        html = HTMLParser(resp.text)

        return int(html.css_first("div.navcent").css("a")[-1].text().strip())


    def parse(self, response, **kwargs):
        for i in response.css("div.shorposterbox"):
            link = i.css("div.postertitle").css("h2").css("a").xpath("@href").get()

            yield scrapy.Request(link, self.parse_film)

    def parse_film(self, response):
        name = response.css("h1[itemprop='name']").xpath("text()").get().split("(")[0].strip()
        year = response.css(
            "ul.janrfall").css("li")[4].xpath("text()").get()
        genres = [i.xpath("text()").get() for i in response.css("ul.janrfall").css("li")[2].css("a")]
        duration = response.css(
            "ul.janrfall").css("li")[6].xpath("text()").get()
        poster = response.css("img[itemprop='image']").xpath("@src").get()

        soup = BeautifulSoup(response.body,  "lxml")
        players = []
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        for i in soup.find_all("iframe"):
            try:
                players.append({
                    f"player": i["src"]
                })
            except:
                pass

        for comment in comments:
            if "iframe" in comment:
                players.append({
                    f"player": comment.split("src=")[1].replace('"', "").split(" ")[0]
                })

        description = soup.find("div", itemprop="description").get_text(separator="\n", strip=True)
        countries = soup.find("ul", class_="janrfall").find_all("li")[5].contents[2].strip().split(',')

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
