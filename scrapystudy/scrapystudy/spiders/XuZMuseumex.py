import scrapy

from ..items import ExhibItem


class XuzmuseumexSpider(scrapy.Spider):
    name = 'XuZMuseumex'
    allowed_domains = ['https://www.xzmuseum.com/']
    start_urls = ['https://www.xzmuseum.com/zl.aspx?category_id=495']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id=10001
    base_url="https://www.xzmuseum.com"
    def parse(self, response):
        list=response.xpath("//div[@class='ny_rd']/div")
        for li in list:
            exh_name=li.xpath(".//h2/a/text()").get()
            exh_picture=li.xpath(".//img/@src").get()
            exh_picture=self.base_url+exh_picture
            detail_url=li.xpath(".//h2/a/@href").get()
            yield scrapy.Request(self.base_url+detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"exh_name":exh_name,"exh_picture":exh_picture})


    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture=response.meta["exh_picture"]
        exh_info=response.xpath("//div[@class='del_f']//text()").getall()
        exh_info="".join(exh_info).strip()
        exh_id="3240"+str(self.Id)
        self.Id+=1
        mus_id=3240
        mus_name="徐州博物馆"
        exh_time="常设"
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item
