from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from utils.database import Database
from utils.parser.parser.spiders.gidonline_spider import GidonlineSpider
from utils.parser.parser.spiders.kinokrad_spider import KinokradSpider
from utils.parser.parser.spiders.kinogo_spider import KinogoSpider
from utils.parser.parser.spiders.kinoprofi_spider import KinoprofiSpider

from urllib.parse import urlparse
import logging
import asyncio

from utils.checker import Checker
from utils.io import IO


def main():
    option = IO.print_menu()

    if option == 1:
        check_support()

    elif option == 2:
        website = IO.input("Please enter the website u want to parse:\n1 - Gidonline\n2 - Kinokrad\n3 - Kinogo\n4 - Kinoprofi")

        settings = get_project_settings()
        process = CrawlerProcess(settings)

        if "1" in website:
            process.crawl(GidonlineSpider)
        elif "2" in website:
            process.crawl(KinokradSpider)
        elif "3" in website:
            process.crawl(KinogoSpider)
        elif "4" in website:
            process.crawl(KinoprofiSpider)

        process.start()

        db = Database()
        db.start()


def check_support():
    # --- DISABLING SCRAPY LOGS ---
    logging.getLogger('scrapy').propagate = False

    website = IO.input("Please enter a link to the website you want to check")
    check_result = Checker.check_support(website)
    IO.output(f"[bold]Is[/bold] [italic]{urlparse(website).netloc}[/italic] [bold]support parser:[/bold] {check_result}")


if __name__ == "__main__":
    main()
