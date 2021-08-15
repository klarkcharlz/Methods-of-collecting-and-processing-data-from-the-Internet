import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    search = 'python'
    start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("///a[contains(@class, 'f-test-button-dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@class='f-test-search-result-item']//a[contains(@class, 'f-test-link-') "
                               "and contains(@href, 'vakansii')]/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        salary_min = response.xpath('//div[contains(@class, "_3MVeX")]//span[contains(@class, "_1h3Zg _2Wp8I")]'
                                    '/text()').extract()
        location = response.xpath('//div[@class="f-test-address _3AQrx"]//text()').extract()
        url = response.url
        company = response.xpath('//div[@class="_3zucV FAfe0 _3fOgw"]//text()').extract_first()
        yield JobparserItem(name=name, salary_min=salary_min, location=location,
                            url=url, company=company)
