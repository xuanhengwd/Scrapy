import scrapy

from ..items import ExhibItem


class FjmuseumexSpider(scrapy.Spider):
    name = 'FJMuseumex'
    allowed_domains = ['http://www.fjbwy.com/']
    start_urls = ['http://www.fjbwy.com/node_23.html']
    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id=10001
    page_id=2
    def parse(self, response):
        list=response.xpath("//div[@class='container_nr']/div[@class='zp_k']")
        for li in list:
            exh_name=li.xpath(".//div[@class='zp_smk']/div[@class='zp_sj']/span/text()").get()
            exh_picture=li.xpath(".//div[@class='zp_tu']/a/img/@src").get()
            exh_time=li.xpath(".//div[@class='zp_smk']/div[@class='zp_sj']/@data-time").get()
            if exh_time=='':
                exh_time='无'
            detail_url=li.xpath(".//div[@class='zp_tu']/a/@href").get()
            yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"exh_name":exh_name,"exh_picture":exh_picture,"exh_time":exh_time})
        next_url="http://www.fjbwy.com/node_23_"+str(self.page_id)+".html"
        self.page_id+=1
        if self.page_id>5:
            return
        else:
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture=response.meta["exh_picture"]
        exh_info=response.xpath("//div[@class='neir_zw']/p//text()").getall()
        exh_info=''.join(exh_info).strip()
        exh_info=''.join(exh_info.split())
        if exh_info=='':
            exh_info='无'

        exh_id="3501"+str(self.Id)
        self.Id+=1
        mus_id=3501
        mus_name='福建博物院'
        exh_time=response.meta["exh_time"]
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item
