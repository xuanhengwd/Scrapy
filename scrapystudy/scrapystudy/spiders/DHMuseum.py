import scrapy

#没有藏品 敦煌
class DhmuseumSpider(scrapy.Spider):
    name = 'DHMuseum'
    allowed_domains = ['https://www.dha.ac.cn/']
    start_urls = ['http://https://www.dha.ac.cn//']

    def parse(self, response):
        pass
