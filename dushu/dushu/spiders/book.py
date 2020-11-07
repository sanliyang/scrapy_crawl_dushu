import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['dushu.com']
    start_urls = ['https://www.dushu.com/book/']

    rules = (
        # 拿到所有图书分类的链接css匹配
        Rule(LinkExtractor(restrict_css='.sub-catalog'),
             follow=True),
        # 分页的href 正则匹配
        Rule(LinkExtractor(r'/book/\d+?_\d+?\.html'),
             follow=True),
        # 图书详情信息的正则匹配
        Rule(LinkExtractor(r'/book/\d+/'),
             'parse_item',
             follow=False)
    )

    def parse_item(self, response):
        item = {}
        item['title'] = response.css('h1::text').get()
        item['cover'] = response.css('.pic img::attr("src")').get()
        item['price'] = response.css('.num::text').get()
        table = response.css('#ctl00_c1_bookleft table')
        item['author'] = table.xpath('./tr[1]/td[2]/text()').get()
        item['pubulisher'] = table.xpath('./tr[2]/td[2]/text()').get()
        table = response.css('.book-details>table')
        item['isbn'] = table.xpath('.//tr[1]/td[2]/text()').get()
        item['time'] = table.xpath('.//tr[1]/td[4]/text()').get()
        item['pages'] = table.xpath('.//tr[2]/td[4]/text()').get()

        yield item




