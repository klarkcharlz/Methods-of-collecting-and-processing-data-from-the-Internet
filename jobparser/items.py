import scrapy


class JobparserItem(scrapy.Item):
    name = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    company = scrapy.Field()
    currency = scrapy.Field()
    _id = scrapy.Field()
