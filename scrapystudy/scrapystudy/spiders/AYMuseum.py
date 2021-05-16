import scrapy

from ..items import CollectionItem

#3605
class AymuseumSpider(scrapy.Spider):
    name = 'AYMuseum'
    allowed_domains = ['http://www.aymuseum.com/']
    start_urls = ['http://www.aymuseum.com/nr.jsp?_jcp=4_2#_np=120_0']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    base_url='http://www.aymuseum.com/'
    Id=10001
    def parse(self, response):
        list=response.xpath("//div[@class='newsList ']/div[@topclassname='top1']")
        for li in list:
            col_name=li.xpath(".//@newsname").get()
            detail_url=li.xpath(".//table/tr/td[@class='newsTitle']/a/@href").get()
            detail_url=self.base_url+detail_url
            yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True)



    def parse_detail(self,response):
        col_info=response.xpath("//div[@class='richContent  richContent0']//text()").getall()
        col_info=''.join(col_info).strip()
        col_name=response.xpath("//div[@class='newsDetail newsDetailV2']/h1/text()").get()
        col_era="在描述里"
        col_picture=response.xpath("//div[@class='richContent  richContent0']/p[1]/span/img/@src").get()
        if col_picture is None:
            col_picture=response.xpath("//div[@class='richContent  richContent0']/p[2]/span/img/@src").get()
        col_picture='Http:'+col_picture
        print(col_picture)
        mus_name="安源路矿工人运动纪念馆"
        col_id="3605"+str(self.Id)
        self.Id+=1
        mus_id=3605
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item

