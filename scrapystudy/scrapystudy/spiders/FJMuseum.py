import scrapy

from ..items import CollectionItem

#3501
class FjmuseumSpider(scrapy.Spider):
    name = 'FJMuseum'
    allowed_domains = ['http://www.fjbwy.com/']
    start_urls = ['http://www.fjbwy.com/node_124.html#nav']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }


    Id=10001
    page_id=2
    def parse(self, response):
        list=response.xpath("//div[@class='container']/div[@class='zstuk']")
        for li in list:
            col_name=li.xpath(".//div[@class='zstusm']/a/text()").get()
            col_picture=li.xpath(".//div[@class='zstu']/a/img/@src").get()
            detail_url=li.xpath(".//div[@class='zstu']/a/@href").get()
            yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"col_picture":col_picture,"col_name":col_name})

        next_url="http://www.fjbwy.com/node_124_"+str(self.page_id)+".html#nav"
        self.page_id+=1
        if self.page_id>20:
            return
        else:
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)

    def parse_detail(self,respnse):
        col_name=respnse.meta["col_name"]
        col_picture=respnse.meta["col_picture"]
        col_info=respnse.xpath("//div[@class='nr_smzw']/p//text()").getall()
        col_info=''.join(col_info).strip()
        col_info=''.join(col_info.split())
        col_era=respnse.xpath("//div[@class='nr_sm_1']/div[3]/text()").get()

        if not col_era:
            col_era="不详或在描述里"
        col_era=col_era.strip()
        mus_name="福建博物院"
        mus_id=3501
        col_id="3501"+str(self.Id)
        self.Id+=1
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item
