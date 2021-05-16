import scrapy

from ..items import ExhibItem


class YtmuseumexSpider(scrapy.Spider):
    name = 'YTmuseumex'
    allowed_domains = ['http://www.ytmuseum.com']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    start_urls = ['http://www.ytmuseum.com/showroom']
    base1_url = "http://www.ytmuseum.com"
    base_url = "http://www.ytmuseum.com/showroom/"
    exhid = ["notice", "jb", "zt", "tb", "hg", "xz", "cg"]
    Id = 10001

    def parse(self, response):
        for i in range(7):
            exh_url = self.base_url + self.exhid[i]
            yield scrapy.Request(exh_url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        list = response.xpath("//div[@id='MainLeft']/div[last()]/div/ul/li")
        for li in list:
            exh_name = li.xpath(".//div[last()]/a/text()").get()
            exh_picture = li.xpath(".//div[1]/a/img/@src").get()
            exh_picture = exh_picture.replace("//", "")
            detail_url = li.xpath(".//div[last()]/a/@href").get()
            detail_url = "http://www.ytmuseum.com" + detail_url
            yield scrapy.Request(detail_url, callback=self.detail, dont_filter=True,
                                 meta={"exh_picture": exh_picture, "exh_name": exh_name})
        next_url = response.xpath("//ul[@class='pagination']/li[last()-1]/a/@href").get()
        if not next_url:
            return
        yield scrapy.Request(self.base1_url + next_url, callback=self.parse_detail, dont_filter=True)

    def detail(self, response):
        exh_name = response.meta['exh_name']
        exh_picture = response.meta['exh_picture']
        exh_info = response.xpath("//div[@id='MainLeft']/div[last()]/div[1]/table/tr[last()]//text()").getall()
        exh_info = "".join(exh_info).strip()
        exh_info="".join(exh_info.split())
        exh_time = "info里"
        mus_name = "烟台市博物馆"
        exh_id = "3706" + str(self.Id)
        self.Id += 1
        mus_id = 3706
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item
