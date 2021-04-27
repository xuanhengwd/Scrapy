

import scrapy
from lxml import etree
from w3lib.html import remove_tags

# 行政代码32   musid 3207
#藏品3207 +五位
from ..items import CollectionItem


class NjmuseumSpider(scrapy.Spider):
    name = 'NjMuseum'
    allowed_domains = ['http://www.njmuseumadmin.com/']
    start_urls = ['http://www.njmuseumadmin.com/Antique/lists/p/1']

    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.NjmuseumPipeline': 300}
    }


    base_url="http://www.njmuseumadmin.com"
    next_url_judge="/Antique/lists/p/1"
    Id=10001
    def parse(self, response):
        lists=response.xpath("//div[@class='Object_listcon']/ul/li")
        for list in lists:
            col_name=list.xpath(".//span/text()").get()
            col_picture=list.xpath(".//img/@src").get()
            col_picture=self.base_url+col_picture
            detail_url=list.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_url+detail_url,callback=self.parse_detail,dont_filter=True,meta={'col_name':col_name,'col_picture':col_picture})

        next_url=response.xpath("//div[@class='pagination']/ul/li/a[@class='next']/@href").get()
        if next_url==self.next_url_judge:
            return
        else:
            self.next_url_judge=next_url
            yield scrapy.Request(self.base_url+next_url,callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        col_id="3207"+str(self.Id)
        self.Id+=1
        mus_id=3207
        col_name=response.meta["col_name"]
        col_picture=response.meta["col_picture"]
        col_era=response.xpath("//div[@class='parameter']/p[1]/text()").get()
        #网上级标签寻找，找到有输出的，然后查看输出文字的标签
        #或者分析网页的结构 判断是第几个标签 用数字代替class
        col_info=response.xpath("//div[@class='basicrightcon']/div[3]").get()
        col_info=remove_tags(col_info)
        mus_name="南京市博物总馆"
        item=CollectionItem(col_id=col_id,mus_id=mus_id,col_name=col_name,col_era=col_era,col_info=col_info,mus_name=mus_name,col_picture=col_picture)
        yield item


