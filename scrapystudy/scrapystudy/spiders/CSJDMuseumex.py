import scrapy

from ..items import ExhibItem


class CsjdmuseumexSpider(scrapy.Spider):
    name = 'CSJDMuseumex'
    allowed_domains = ['http://www.chinajiandu.cn/']
    start_urls = ['http://www.chinajiandu.cn/Exhibition/TList/lszl']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }


    typeid=1
    Id=10001
    def parse(self, response):
        list=response.xpath("//ul[@class='tempexhlist']/li")
        for li in list:
            exh_name=li.xpath(".//div[@class='cont']/a/h3/text()").get().strip()
            exh_picture=li.xpath(".//a/div/img/@src").get()
            exh_time=li.xpath(".//div[@class='cont']/div[@class='intro']/p[1]/text()").get()
            detail_url=li.xpath(".//a/@href").get()
            detail_url="http://www.chinajiandu.cn"+detail_url
            yield scrapy.Request(detail_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"exh_name": exh_name, "exh_picture": exh_picture,"exh_time":exh_time})

        next_url=response.xpath("//ul[@class='pages']/li[last()-1]/a/@href").get()
        if not next_url:
            return
        else:

            next_url="http://www.chinajiandu.cn"+next_url
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture=response.meta["exh_picture"]
        exh_time=response.meta["exh_time"]
        exh_info=response.xpath("//div[@class='cont']//text()").getall()
        exh_info=''.join(exh_info).strip()
        exh_id="4304"+str(self.Id)
        self.Id+=1
        mus_id=4304
        mus_name="长沙简牍博物馆"

        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item