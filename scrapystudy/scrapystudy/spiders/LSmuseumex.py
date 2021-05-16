import scrapy

from ..items import ExhibItem


class LsmuseumexSpider(scrapy.Spider):
    name = 'LSmuseumex'
    allowed_domains = ['http://www.lvshunmuseum.org/']
    start_urls = ['http://www.lvshunmuseum.org/Exhibition/?SortID=2']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id = 10001
    base_url = "http://www.lvshunmuseum.org"

    def parse(self, response):
        list = response.xpath("//div[@class='new_show']/ul/li")
        for li in list:
            exh_name = li.xpath(".//a/div[@class='textbox']/h1/text()").get()
            exh_picture = li.xpath(".//a/div[@class='picbox']/img/@src").get().strip()
            exh_picture = self.base_url + exh_picture
            detail_url = li.xpath(".//a/@href").get().strip()
            yield scrapy.Request(self.base_url + detail_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"exh_name": exh_name, "exh_picture": exh_picture})
        next_url = response.xpath("//div[@class='pagination']/a[@class='page_next']/@href").get()
        if next_url == 'javascript:;':
            return
        yield scrapy.Request(self.base_url + next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        exh_name = response.meta["exh_name"]
        exh_picture = response.meta["exh_picture"]
        exh_info = response.xpath("//div[@class='textshow']//text()").getall()
        exh_info = "".join(exh_info).strip()
        exh_info = "".join(exh_info.split())
        exh_info = exh_info.replace("详细介绍", "")
        if exh_info == '':
            exh_info = "无"
        exh_id = "2104" + str(self.Id)
        self.Id += 1
        mus_id = 2104
        mus_name = "旅顺博物馆"
        exh_time = "常设"
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item