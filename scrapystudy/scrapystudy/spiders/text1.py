import scrapy

from ..items import Text1Item


class Text1Spider(scrapy.Spider):
    name = 'text1'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    Id=1
    def parse(self, response):
        id=self.Id
        num=3
        name="cfr"
        item=Text1Item(id=id,num=num,name=name)
        yield item
