import scrapy
from ..items import DuanziItem
from scrapy.http.response.html import HtmlResponse


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain = "https://www.qiushibaike.com"

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.DuanziPipleline':300},
    }
    # SelectorList
    def parse(self, response):
        duanzidivs = response.xpath("//div[@class='col1 old-style-col1']/div")
        for duanzidiv in duanzidivs:
            # Selector
            author = duanzidiv.xpath(".//h2/text()").get().strip()
            content = duanzidiv.xpath(".//div[@class='content']//text()").getall()
            # 变成字符串
            content = "".join(content).strip()
            item = DuanziItem(author=author, content=content)
            # 字典
            # duanzi={
            #     "author":author,
            #     "content":content
            # }
            # yield duanzi
            yield item
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse)
