import scrapy

from ..items import ExhibItem


class ZgdymuseumexSpider(scrapy.Spider):
    name = 'ZGDYMuseumex'
    allowed_domains = ['http://www.cnfm.org.cn/']
    start_urls = ['http://www.cnfm.org.cn/ybzl/ztzl.shtml']
    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id=10001
    base_url="http://www.cnfm.org.cn"
    def parse(self, response):
        body=response.xpath("/html/body/table[1]/tr/td/table[2]/tr/td/table/tr[3]/td[2]/table/tr/td/table/tr")
        for tr in body:
            tds=tr.xpath(".//td")
            for td in tds:
                exh_name=td.xpath(".//div/p/a/text()").get()
                if not exh_name or exh_name=='  ':
                    break
                exh_picture=td.xpath(".//div/a/img/@src").get()
                exh_picture=self.base_url+exh_picture
                exh_id="1140"+str(self.Id)
                self.Id+=1
                mus_id=1140
                mus_name="中国电影博物馆"
                exh_info=exh_name
                exh_time="无"
                item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                                 exh_picture=exh_picture, exh_time=exh_time)
                yield item

