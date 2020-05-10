import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import ScrapingquotesItem

class QuotesSpider(scrapy.Spider):

    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/login']
    item = ScrapingquotesItem()

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response,
                                        formdata = {
                                            'csrf_token': token,
                                            'username': 'username',
                                            'password': 'password'
                                        }, callback = self.scraping_process)


    def scraping_process(self, response):
        all_divs = response.css('div.quote')

        for div in all_divs:
            QuotesSpider.item['quote'] = div.css('span.text::text').extract()
            QuotesSpider.item['author'] = div.css('.author::text').extract()
            QuotesSpider.item['tags'] = div.css('.tag::text').extract()
            yield QuotesSpider.item

        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            # open_in_browser(response)
            # Execute the parse function after following the path next_page
            yield response.follow(next_page, callback = self.scraping_process)