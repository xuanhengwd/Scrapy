import scrapy
from ..items import ScrapystudyItem
from scrapy.http.response.html import HtmlResponse


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    # SelectorList
    def parse(self, response):
        duanzidivs = response.xpath("//div[@class='col1 old-style-col1']/div")
        for duanzidiv in duanzidivs:
            # Selector
            author = duanzidiv.xpath(".//h2/text()").get().strip()
            content = duanzidiv.xpath(".//div[@class='content']//text()").getall()
            # 变成字符串
            content = "".join(content).strip()
            item = ScrapystudyItem(author=author, content=content)
            # 字典
            # duanzi={
            #     "author":author,
            #     "content":content
            # }
            # yield duanzi
            yield item
