import scrapy

from ..items import ExhibItem


class SxlsmuseumexSpider(scrapy.Spider):
    name = 'SXLSMuseumex'
    allowed_domains = ['http://www.sxhm.com/']
    start_urls = ['http://www.sxhm.com/index.php?page=1&ac=article&at=list&tid=196']

    custom_settings = {
        "ITEM_PIPELINES": {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id=10001
    base_url='http://www.sxhm.com'
    def parse(self, response):
        piclist=response.xpath("//div[@class='maintxt']/ul/li")
        for li in piclist:
            detail_url=li.xpath(".//a/@href").get()
            yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True)
        next_url=response.xpath("//div[@class='page']/ul/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)


    def parse_detail(self,response):
        exh_name=response.xpath("//div[@class='bt']/text()").get().strip()
        exh_info=response.xpath("//div[@class='p']//text()").getall()
        exh_info=''.join(exh_info).strip()
        exh_time="在描述里"
        exh_picture=''
        exh_pictures=response.xpath("//div[@class='p']/p")
        for i in exh_pictures:
            exh_picture=i.xpath(".//img/@src").get()
            if exh_picture:
                break
        if not exh_picture:
            exh_picture="无"
        else:
            exh_picture=self.base_url+exh_picture
            print(exh_picture)
        exh_id="6101"+str(self.Id)
        self.Id+=1
        mus_id=6101
        mus_name="陕西历史博物馆"
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item