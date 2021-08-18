import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_price(value):
    value = int(value.replace(' ', ''))
    return value


def process_feature(value):
    return value


class LeroymerlinParserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price))
    photos = scrapy.Field()
    url = scrapy.Field()
    feature = scrapy.Field(input_processor=MapCompose(process_feature))

