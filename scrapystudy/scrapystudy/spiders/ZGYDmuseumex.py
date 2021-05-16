import scrapy

from ..items import ExhibItem


class ZgydmuseumexSpider(scrapy.Spider):
    name = 'ZGYDmuseumex'
    allowed_domains = ['http://www.zgyd1921.com/']
    start_urls = ['http://www.zgyd1921.com/zgyd/node3/n11/n13/index.html']


    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id=10001
    base_url = "http://www.zgyd1921.com"
    def parse(self, response):
        list=response.xpath("//ul[@class='piclist3']/li")
        for li in list:
            exh_name=li.xpath(".//div/p[@class='name']/a/text()").get().strip()
            exh_picture=li.xpath(".//a/img/@src").get()
            exh_picture=self.base_url+exh_picture
            url=li.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_url+url,callback=self.parse_detail,dont_filter=True,
                                 meta={"exh_name":exh_name,"exh_picture":exh_picture})


    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture=response.meta["exh_picture"]
        exh_info_url=response.xpath("//div[@class='fc']/iframe/@src").get()
        yield scrapy.Request(self.base_url+exh_info_url,callback=self.parse_page,meta={"exh_name":exh_name,"exh_picture":exh_picture},dont_filter=True)

    def parse_page(self,response):
        exh_info=response.xpath("//div[@class='grey14']/p//text()").getall()
        exh_info="".join(exh_info).strip()
        exh_name=response.meta["exh_name"]
        exh_picture=response.meta["exh_picture"]
        exh_time="常设"
        exh_id="3103"+str(self.Id)
        self.Id+=1
        mus_id=3103
        mus_name='中共一大会址纪念馆'
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item