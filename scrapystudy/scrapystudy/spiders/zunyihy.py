import scrapy
from scrapy import Selector

from ..items import ScrapystudyItem


class ZunyihySpider(scrapy.Spider):
    name = 'zunyihy'
    allowed_domains = ['http://www.zunyihy.cn/']
    start_urls = [
        'http://www.zunyihy.cn/searchs/collection.html?0.17377033055156654&category_id=&tpl_file=collection&content=&pagesize=9&sort=&p=1']
    base_domain = "http://www.zunyihy.cn"

    def parse(self, response):
        cangpins = response.xpath("//div[@class='list_wenchuang']/div")

        for cangpin in cangpins:
            #item=ScrapystudyItem()
            name = cangpin.xpath(".//div[@class='t4 ellipsis']//text()").get()
            image=cangpin.xpath(".//div[@class='img']/img/@src").get()
            image=self.base_domain+image
            img_url=cangpin.xpath(".//a/@href").get()
            #item = ScrapystudyItem(name=name,image=image)
            yield scrapy.Request(self.base_domain+img_url,callback=self.parse_detail,dont_filter=True,meta={"name":name,"image":image})
            #yield item

        next_url = response.xpath("//ul[@class='page-box p-show clear']/li[@class='page-item next']/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse,dont_filter=True)
    def parse_detail(self,response):
        name=response.meta["name"]
        image=response.meta["image"]
        introduction=response.xpath("//div[@class='situation_1']//text()").getall()
        introduction="".join(introduction).strip()
        item=ScrapystudyItem(name=name,image=image,introduction=introduction)
        yield item
