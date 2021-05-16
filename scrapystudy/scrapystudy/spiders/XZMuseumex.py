import scrapy
from w3lib.html import remove_tags

from ..items import ExhibItem


class XzmuseumexSpider(scrapy.Spider):
    name = 'XZMuseumex'
    allowed_domains = ['www.tibetmuseum.com.cn']
    start_urls = ['http://39.106.176.234//api/exhibition/list?p=w&language=1&type=1&skip=0&take=3']

    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    base_url = 'http://www.tibetmuseum.com.cn'
    Id=10001
    def parse(self, response):
        Body=response.json()
        data=Body["data"]
        list1=data["exhibition_index_list"]
        list2=data["exhibition_list"]
        for li1 in list1:
            exh_name=li1["title"]
            exh_picture=li1["list_img"]
            exh_picture=self.base_url+exh_picture
            exh_info=li1["content"]
            exh_info=remove_tags(exh_info).strip()
            exh_id="5401"+str(self.Id)
            self.Id+=1
            mus_id=5401
            mus_name="西藏博物馆"
            exh_time="常设"
            item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                             exh_picture=exh_picture, exh_time=exh_time)
            print(item)
            yield item


        for li2 in list2:
            exh_name=li2["title"]
            exh_picture=li2["list_img"]
            exh_picture=self.base_url+exh_picture
            exh_info=li2["content"]
            exh_info=remove_tags(exh_info).strip()
            exh_id="5401"+str(self.Id)
            self.Id+=1
            mus_id=5401
            mus_name="西藏博物馆"
            exh_time="常设"
            item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                             exh_picture=exh_picture, exh_time=exh_time)
            print(item)
            yield item