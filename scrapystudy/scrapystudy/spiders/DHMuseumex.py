import scrapy

from ..items import ExhibItem

#6203
class DhmuseumexSpider(scrapy.Spider):
    name = 'DHMuseumex'
    allowed_domains = ['https://www.dha.ac.cn/']
    start_urls = ['http://public.dha.ac.cn/list.aspx?id=864012277860']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id=10001
    base_url="http://public.dha.ac.cn/"
    def parse(self, response):
        list=response.xpath("/html/body/div[2]/div[2]/div/ul/table/table/tr")
        for li in list:
            exh_name=li.xpath(".//td/li/a/text()").get().strip()
            detail_url=li.xpath(".//td/li/a/@href").get()
            yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"exh_name":exh_name})


    def parse_detail(self,response):
        exh_name=response.meta["exh_name"]
        exh_picture_xp=response.xpath("/html/body/div[2]/div/div[2]/div[4]")

        exh_info=''
        exh_picture=''
        if not exh_picture_xp:
            exh_picture_xp=response.xpath("/html/body/div[2]/div[2]/div[1]/div[3]")
            exh_picture=response.xpath("//div[@class='image']/img/@src").get()
            exh_info=response.xpath("/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/p/font//text").getall()
        else:
            exh_info = response.xpath("/html/body/div[2]/div/div[2]/div[4]/p/font//text()").getall()
            exh_picture_p=exh_picture_xp.xpath(".//p")
            for i in exh_picture_p:
                exh_picture=i.xpath(".//span/img/@src").get()
                if exh_picture:
                    break
                exh_picture=i.xpath(".//font/img/@src").get()
                if exh_picture:
                    break
                exh_picture = i.xpath(".//img/@src").get()
                if exh_picture:
                    break
        if not exh_picture:
            exh_picture="无"
        else:
            exh_picture=exh_picture.replace("../","")
            exh_picture=self.base_url+exh_picture


        exh_info=''.join(exh_info).strip()
        exh_info=''.join(exh_info.split("\n")).strip()
        print("*"*40)
        if not exh_info:
            exh_info=response.xpath("/html/body/div[2]/div/div[2]/div[4]/p/span//text()").getall()
            exh_info = ''.join(exh_info).strip()
            exh_info = ''.join(exh_info.split("\n")).strip()
        if not exh_info:
            exh_info = response.xpath("/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/p/font//text()").getall()
            exh_info = ''.join(exh_info).strip()
            exh_info = ''.join(exh_info.split("\n")).strip()
        if not exh_info:
            exh_info = response.xpath("/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/p/span//text()").getall()
            exh_info = ''.join(exh_info).strip()
            exh_info = ''.join(exh_info.split("\n")).strip()

        exh_time="常设"
        mus_name="敦煌研究院"
        mus_id="6203"
        exh_id="6203"+str(self.Id)
        self.Id+=1
        item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                         exh_picture=exh_picture, exh_time=exh_time)
        yield item