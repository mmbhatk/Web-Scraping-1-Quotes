import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import ScrapingquotesItem

class QuotesSpider(scrapy.Spider):
    def __init__(self):
        self.item = ScrapingquotesItem()

    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response,
                                        formdata = {
                                            'csrf_token': token,
                                            'username': 'abcd',
                                            'password': 'pass'
                                        }, callback = self.scraping_process)


    def scraping_process(self, response):
        all_divs = response.css('div.quote')

        for div in all_divs:
            self.item['quote'] = div.css('span.text::text').extract()
            self.item['author'] = div.css('.author::text').extract()
            self.item['tags'] = div.css('.tag::text').extract()
            yield self.item

        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            open_in_browser(response)
            # Execute the parse function after following the path next_page
            yield response.follow(next_page, callback = self.scraping_process)