import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        # 'https://quotes.toscrape.com/tag/humor/',
        'https://www.maoyan.com/cinema/181',
    ]

    def parse(self, response):
        print(123)
        print(response)
        for quote in response.css('div.show-date'):
            print(quote)
            yield {
                'date': quote.xpath('span/text()').get(),
            }

# scrapy runspider quotes_spider.py -o quotes.jsonl