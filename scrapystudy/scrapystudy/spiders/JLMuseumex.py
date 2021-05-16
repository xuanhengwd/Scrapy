import scrapy

from ..items import ExhibItem


class JlmuseumexSpider(scrapy.Spider):
    name = 'JLMuseumex'
    allowed_domains = ['http://www.jlmuseum.org/']
    start_urls = ['http://www.jlmuseum.org/display/']

    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id = 10001
    base_url = "http://www.jlmuseum.org/"
    def parse(self, response):
        list=response.xpath("//div[@class='list']/ul/li")
        for li in list:
            exh_picture=li.xpath(".//a/img/@src").get()
            exh_picture=self.base_url+exh_picture
            exh_name=li.xpath(".//div[@class='i']/a/text()").get()
            exh_name=exh_name.strip()
            detail_url=li.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_url+detail_url,callback=self.parse_detail,dont_filter=True,meta={'exh_picture':exh_picture,'exh_name':exh_name})

    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture=response.meta["exh_picture"]
        exh_id = "2202" + str(self.Id)
        self.Id += 1
        mus_id = 2202
        mus_name = "吉林省博物院"
        exh_info=response.xpath("//div[@class='pics-cont']//text()").getall()
        exh_info="".join(exh_info).strip()
        exh_time="正在进行"
        item=ExhibItem(exh_id=exh_id,exh_name=exh_name,mus_id=mus_id,mus_name=mus_name,exh_info=exh_info,exh_picture=exh_picture,exh_time=exh_time)
        yield item