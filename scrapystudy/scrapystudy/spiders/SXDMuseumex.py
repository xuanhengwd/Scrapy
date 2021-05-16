import scrapy

from ..items import ExhibItem


class SxdmuseumexSpider(scrapy.Spider):
    name = 'SXDMuseumex'
    allowed_domains = ['http://www.sxd.cn']
    start_urls = ['http://www.sxd.cn/list_1.asp?bigclass=23']

    custom_settings = {
        "ITEM_PIPELINES": {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    base_url="http://www.sxd.cn/"
    Id=10001
    def parse(self, response):
        list1=response.xpath("/html/body/div/div[2]/div[2]/table[2]/tr/td[2]/table")
        list2=list1.xpath(".//tr[2]/td/table/tr/td/table")
        list=list2.xpath(".//tr/td/table/tr")
        for li in list:
            exh_name=li.xpath(".//td/a/text()").get()
            detail_url=li.xpath(".//td/a/@href").get()
            if not exh_name:
                continue
            detail_url=self.base_url+detail_url
            yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"exh_name":exh_name})

        next_url = list2.xpath(".//tr/td/table/tr[last()]/td/table/tr/td/a[last()-1]/@href").get()
        last_url = list2.xpath(".//tr/td/table/tr[last()]/td/table/tr/td/a[last()]/@href").get()
        if next_url[14:16] > last_url[14:16]:
            return
        else:
            next_url = "http://www.sxd.cn/list_1.asp" + next_url
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)


    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture=''
        exh_xp=response.xpath("/html/body/div/div[2]/div[2]/table[2]/tr/td[2]/table/tr[2]/td/table/tr[2]")
        exh_picture_p=exh_xp.xpath(".//td/p")
        for i in exh_picture_p:
            exh_picture=i.xpath(".//img/@src").get()
            if exh_picture:
                break
        if not exh_picture:
            exh_picture=exh_xp.xpath(".//td/img/@src").get()
        if not exh_picture:
            exh_picture="无"
        exh_info=exh_xp.xpath(".//td/p//text()").getall()

        if not exh_info:
            exh_info=exh_xp.xpath(".//td/span//text()").getall()
        if not exh_info:
            exh_info=exh_xp.xpath(".//td[1]//text()").getall()
            exh_info="".join(exh_info).strip()
            exh_info=exh_info.split()
            exh_info=exh_info[0]
        exh_info = "".join(exh_info).strip()

        exh_id="5102"+str(self.Id)
        self.Id+=1
        mus_id=5102
        mus_name="三星堆博物馆"
        exh_time="常设"
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item
