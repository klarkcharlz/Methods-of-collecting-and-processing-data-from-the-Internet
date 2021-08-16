import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru/']

    def __init__(self, search):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-marker='item-title']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath("name", "//h1/span/text()")
        loader.add_xpath("photos", "//div[@class='gallery-img-frame js-gallery-img-frame']/@data-url")
        loader.add_xpath("stats", "")
        loader.add_xpath("price", "")
        loader.add_value("url", response.url)

        yield loader.load_item()
