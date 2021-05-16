import scrapy


class AymuseumexSpider(scrapy.Spider):
    name = 'AYMuseumex'
    allowed_domains = ['http://www.aymuseum.com/']
    start_urls = ['http://http://www.aymuseum.com//']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    def parse(self, response):
        pass
