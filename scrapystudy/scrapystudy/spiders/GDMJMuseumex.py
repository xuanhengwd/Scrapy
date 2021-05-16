import scrapy
from w3lib.html import remove_tags

from ..items import ExhibItem


class GdmjmuseumexSpider(scrapy.Spider):
    name = 'GDMJMuseumex'
    allowed_domains = ['https://www.gzchenjiaci.com/']
    start_urls = ['https://www.gzchenjiaci.com/MYwebsite/rc/findQDEHView?page=1&size=6&ehTypes=2']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }
    flag=0
    Id=10001
    base_url = "https://www.gzchenjiaci.com/MYwebsite"
    def parse(self, response):

        self.flag+=1
        Body=response.json()
        print(Body)
        data=Body["data"]
        for dect in data:
            exh_name=dect["ehName"]
            exh_picture=dect["ehImg"]
            exh_picture=self.base_url+exh_picture
            exh_info=dect["ehContent"]
            exh_info=remove_tags(exh_info)
            exh_info=exh_info.replace("&nbsp;","").strip()
            exh_id='4406'+str(self.Id)
            self.Id+=1
            mus_id=4406
            mus_name="广东民间工艺博物馆"
            exh_time="常设"
            if self.flag==3:
                exh_time="正在展览"
                exh_info=dect["ehSummary"]
            item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                             exh_picture=exh_picture, exh_time=exh_time)
            yield item
        if self.flag==2:
            url="https://www.gzchenjiaci.com/MYwebsite/rc/findQDEHView?page=1&size=3&ehTypes=0"
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)
        elif self.flag==3:
            return
        else:
            next_url="https://www.gzchenjiaci.com/MYwebsite/rc/findQDEHView?page=2&size=6&ehTypes=2"
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)
