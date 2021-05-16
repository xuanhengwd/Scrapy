import scrapy

from ..items import ExhibItem


class LfmuseumexSpider(scrapy.Spider):
    name = 'LFMuseumex'
    allowed_domains = ['http://www.linfenmuseum.com/']
    start_urls = ['http://www.linfenmuseum.com/index.php/Index/exhibition.html#']
    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    base_url="http://www.linfenmuseum.com"
    Id=10001
    def parse(self, response):
        list=response.xpath("//div[@class='temporaryList current']/a")
        for li in list:
            exh_name=li.xpath(".//div[@class='item_right']/text()").get()
            detail_url=li.xpath(".//@href").get()
            yield scrapy.Request(self.base_url+detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"exh_name":exh_name})

    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture=response.xpath("//div[@class='full-right W680 bordertop1 pt15']/p[1]/img/@src").get()
        if not exh_picture:
            exh_picture=response.xpath("//div[@class='full-right W680 bordertop1 pt15']/p[1]/span/img/@src").get()
        exh_picture=self.base_url+exh_picture
        exh_info=response.xpath("//div[@class='full-right W680 bordertop1 pt15']//text()").getall()
        exh_info=''.join(exh_info).strip()
        exh_id="1140"+str(self.Id)
        self.Id+=1
        mus_id=1140
        mus_name='临汾市博物馆'
        exh_time="无"
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item