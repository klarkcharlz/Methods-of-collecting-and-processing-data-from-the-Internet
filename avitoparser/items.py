import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_photo_url(value):
    return value


class LeroymerlinItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photo_url))
    stats = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field()
