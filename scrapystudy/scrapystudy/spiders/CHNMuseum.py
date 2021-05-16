import scrapy


class ChnmuseumSpider(scrapy.Spider):
    name = 'CHNMuseum'
    allowed_domains = ['http://www.chnmuseum.cn/']
    start_urls = ['http://www.chnmuseum.cn/zp/zpml/kgdjp/']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    def parse(self, response):
        print(1)
        list=response.xpath("//ul[@class='cj_com_zhanchu cj_mb20']/li")
        for li in list:
            print(1)
