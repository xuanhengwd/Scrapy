import scrapy

from ..items import CollectionItem

#5101
class ZgklmuseumSpider(scrapy.Spider):
    name = 'ZGkLMuseum'
    allowed_domains = ['http://www.zdm.cn']
    start_urls = ['http://www.zdm.cn/treasure.html']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id=10001
    def parse(self, response):
        body=response.xpath("/html/body").get()
        divs=response.xpath("//div[@class='swiper-wrapper']/div")
        for div in divs:
            list=div.xpath(".//div[@class='row listItemBox']/div")
            for li in list:
                col_name=li.xpath(".//a/p/text()").get()
                col_picture=li.xpath(".//a/div/img/@src").get()
                detail_url=li.xpath(".//a/@href").get()
                detail_url="http://www.zdm.cn/"+detail_url
                yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,
                                     meta={"col_name":col_name,"col_picture":col_picture})


    def parse_detail(self,response):
        col_name=response.meta["col_name"]
        col_picture=response.meta["col_picture"]
        col_info=response.xpath("//div[@class='textBox']//text()").getall()
        col_info=''.join(col_info).strip()
        col_era=response.xpath("//div[@class='textBox']/p[3]//text()").getall()
        col_era=''.join(col_era).strip()
        if "时" not in col_era:
            col_era = response.xpath("//div[@class='textBox']/p[4]//text()").getall()
            col_era = ''.join(col_era).strip()
        col_id="5101"+str(self.Id)
        self.Id+=1
        mus_id=5101
        mus_name="自贡恐龙博物馆"

        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item