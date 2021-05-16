import scrapy

from ..items import ExhibItem


class ZgklmuseumexSpider(scrapy.Spider):
    name = 'ZGkLMuseumex'
    allowed_domains = ['http://www.zdm.cn']
    start_urls = ['http://www.zdm.cn/cooperation.html']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    base_url="http://www.zdm.cn"
    Id=10001
    def parse(self, response):
        list=response.xpath("//div[@class='row listBox']/div")
        for li in list:
            exh_name=li.xpath(".//a/p[@class='title']/text()").get()
            exh_picture=li.xpath(".//a/div[@class='imgBox']/img/@src").get()
            detail_url=li.xpath(".//a/@href").get()
            detail_url=self.base_url+detail_url
            yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"exh_name":exh_name,"exh_picture":exh_picture})

        next_url=response.xpath("//div[@class='page']/li[last()]/a/@href").get()
        if not next_url:
            return
        yield scrapy.Request(self.base_url+next_url,callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture=response.meta["exh_picture"]
        exh_info=response.xpath("//div[@class='textBox']//text()").getall()
        exh_info=''.join(exh_info).strip()
        exh_id="5101"+str(self.Id)
        self.Id+=1
        mus_id=5101
        mus_name="自贡恐龙博物馆"
        exh_time="描述里"
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item
