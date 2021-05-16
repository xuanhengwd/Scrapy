import scrapy

from..items import CollectionItem

#1140
class ZgdymuseumSpider(scrapy.Spider):
    name = 'ZGDYMuseum'
    allowed_domains = ['http://www.cnfm.org.cn/']
    start_urls = ['http://www.cnfm.org.cn/gcjp/gcjp.shtml']
    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id=10001
    base_url="http://www.cnfm.org.cn"
    def parse(self, response):
        body=response.xpath("/html/body/table[1]/tr/td/table[2]/tr/td/table/tr[3]/td[2]/table/tr/td/table/tr")
        for tr in body:
            tds=tr.xpath(".//td")
            for td in tds:
                col_name=td.xpath(".//div/p/a/text()").get()
                col_picture=td.xpath(".//div/a/img/@src").get()
                col_picture=self.base_url+col_picture
                col_era="无"
                col_info=col_name
                mus_name="中国电影博物馆"
                mus_id=1140
                col_id="1140"+str(self.Id)
                self.Id+=1

                item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era,
                                      col_info=col_info,
                                      mus_name=mus_name, col_picture=col_picture)
                yield item

                # detail_url=td.xpath(".//div/a/@href").get()
                # detail_url=self.base_url+detail_url
                # yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,
                #                      meta={"col_name":col_name,"col_picture":col_picture})



    # def parse_detail(self,response):
    #     col_name=response.meta["col_name"]
    #     col_picture=response.meta["col_picture"]
    #     col_info=