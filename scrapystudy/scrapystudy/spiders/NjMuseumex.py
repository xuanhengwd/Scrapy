import scrapy

from ..items import ExhibItem


class NjmuseumexSpider(scrapy.Spider):
    name = 'NjMuseumex'
    allowed_domains = ['http://www.njmuseumadmin.com/']
    start_urls = ['http://www.njmuseumadmin.com/Exhibition/index/id/40']
    base_urls="http://www.njmuseumadmin.com"
    last_url="/Exhibition/preview/id/40"
    Id = 10001
    custom_settings = {
        "ITEM_PIPELINES":{'scrapystudy.pipelines.MuseumExPipeline':300}
    }
    def parse(self, response):
        exhs=response.xpath("//div[@class='Ex_right_con']/div")
        for exh in exhs:
            detail_url=exh.xpath(".//a/@href").get()
            if detail_url==self.last_url:
                break
            yield scrapy.Request(self.base_urls+detail_url,callback=self.parse_detail,dont_filter=True)
    def parse_detail(self,response):
        exh_name=response.xpath("//div[@class='ex-info-rightcon']/span/text()").get()
        exh_time=response.xpath("//div[@class='ex-info-rightcon']/dl/dt/b/text()").get()
        mus_name="南京市博物总馆"
        exh_info=response.xpath("//div[@class='Ex_content_bottom']//text()").getall()
        exh_picture_url=response.xpath("//div[@class='ex-info-leftcon']/img/@src").get()
        exh_picture=self.base_urls+exh_picture_url
        exh_info="".join(exh_info).strip()
        mus_id=3207
        exh_id="3207"+str(self.Id)
        self.Id+=1
        item=ExhibItem(exh_id=exh_id,exh_name=exh_name,mus_id=mus_id,mus_name=mus_name,exh_info=exh_info,exh_picture=exh_picture,exh_time=exh_time)
        return item
