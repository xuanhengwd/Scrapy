import scrapy

from ..items import CollectionItem
#6101

class SxlsmuseumSpider(scrapy.Spider):
    name = 'SXLSMuseum'
    allowed_domains = ['http://www.sxhm.com/']
    start_urls = ['http://www.sxhm.com/index.php?ac=article&at=list&tid=218']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id=10001
    base_url="http://www.sxhm.com/"
    def parse(self, response):
        list=response.xpath("//ul[@class='piclist']/li")
        for li in list:
            col_name=li.xpath(".//a/span/text()").get()
            col_picture=li.xpath(".//a/img/@src").get()
            col_picture=self.base_url+col_picture
            detail_url=li.xpath(".//a/@href").get()
            yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"col_name":col_name,"col_picture":col_picture})

        next_url=response.xpath("//div[@class='page']/ul/li[last()]/a/@href").get()
        if not next_url:
            return
        yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        col_name=response.meta["col_name"]
        col_picture=response.meta["col_picture"]
        col_info=response.xpath("//div[@class='p']//text()").getall()
        col_info=''.join(col_info).strip()
        col_info=col_info.replace("\\","")
        col_info=''.join(col_info.split("\n")).strip()
        mus_name="陕西历史博物馆"
        col_era="在描述里"
        col_id="6101"+str(self.Id)
        self.Id+=1
        mus_id=6101
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item