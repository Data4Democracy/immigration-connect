# -*- coding: utf-8 -*-
import scrapy

class BlogSpider(scrapy.Spider):
    name = "blog"
    #allowed_domains = ["https://www.whitehouse.gov"]
    #start_urls = ['http://https://www.whitehouse.gov/blog/']

    def __init__(self, limit):
        self.limit = int(limit)

    def start_requests(self):
        start_urls = ['https://www.whitehouse.gov/blog/']
        # main landing page only
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_landing_page) 

    def parse_landing_page(self, response):
        # parse each entry
        urls = response.xpath('//h3[@class="field-content"]/a/@href').extract()
        if urls:
            for url in urls:
                yield scrapy.Request(response.urljoin(url), 
                                     callback=self.parse_article)

	# Read next page
        next_page = response.xpath('//li[@class="pager-next last"]/a/@href'
                                  ).extract_first()
        if next_page is not None:
            if int(next_page.split('=')[-1]) <= self.limit:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page,
                                     callback=self.parse_landing_page)
        pass

    def parse_article(self, response):
        # Title
        title = response.xpath('//h1/text()').extract_first()

        # Date
        date = response.xpath(
            "//div[@id='press_article_date_created']/text()"
        ).extract_first()

        # Text
        text = response.xpath("//p/text()").extract()
        text = [s.strip('\n').strip('\t') for s in text 
                if len(s.strip('\n').strip('\t'))>1 and 
                not s.strip('\n').strip('\t').isspace()]
        text = ' '.join(text)

        # Reference link
        ref = response.xpath("//div/p/a/@href").extract_first() 
        
        yield {
            'title'     : title,
            'date'      : date,
            'text'      : text,
            'origin'    : response,
            'citation'  : ref,
        }
