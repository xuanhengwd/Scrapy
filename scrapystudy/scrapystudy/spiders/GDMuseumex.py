import scrapy

from ..items import ExhibItem


class GdmuseumexSpider(scrapy.Spider):
    name = 'GDMuseumex'
    allowed_domains = ['http://www.gdmuseum.com']
    start_urls = ['http://www.gdmuseum.com/gdmuseum/_300730/_300734/index.html']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id=10001
    base_url="http://www.gdmuseum.com"
    def parse(self, response):
        list=response.xpath("//div[@class='product_w']/div")
        for li in list:
            exh_name=li.xpath(".//a/dl/dt/text()").get().strip()
            exh_picture=li.xpath(".//a/img/@src").get()
            exh_picture=self.base_url+exh_picture
            detail_url=li.xpath(".//a/@href").get().strip()
            yield scrapy.Request(self.base_url+detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"exh_name":exh_name,"exh_picture":exh_picture})

        next_url=response.xpath("//div[@class='paging']/a[@class='next']/@tagname").get()
        if next_url=="[NEXTPAGE]":
            return
        else:
            yield scrapy.Request(self.base_url+next_url,callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture=response.meta["exh_picture"]
        exh_info=response.xpath("//ul[@class='gov_banner_bar']/li[@id='menu_list2']/div[@class='zl_cont']//text()").getall()
        exh_info="".join(exh_info).strip()
        mus_id=4401
        exh_id="4401"+str(self.Id)
        self.Id+=1
        exh_time="正在热展"
        mus_name='广东省博物馆'
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item

