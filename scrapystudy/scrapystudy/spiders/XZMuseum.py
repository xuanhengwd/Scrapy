import scrapy
from w3lib.html import remove_tags

from ..items import CollectionItem

#5401
class XzmuseumSpider(scrapy.Spider):
    name = 'XZMuseum'
    allowed_domains = ['www.tibetmuseum.com.cn']
    start_urls = ['http://39.106.176.234//api/exhibit/exhibit_list?p=w&language=1&skip=0&take=6&class=1']
    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id=10001
    base_url='http://www.tibetmuseum.com.cn'
    classid=2
    def parse(self, response):
        Body=response.json()
        data=Body["data"]
        list=data["exhibit_list"]
        for li in list:
            col_name=li["title"]
            col_picture=li["list_img"]
            col_picture=self.base_url+col_picture
            col_info=li['content']
            if not col_info:
                col_info="无"
            col_info=remove_tags(col_info).strip()
            col_era=li["exhibit_attribute"]
            if not col_era:
                col_era="不详"
            else:
                col_era="".join(col_era).strip()
                col_era=col_era.split()
                col_era=col_era[0]

            col_id="5401"+str(self.Id)
            self.Id+=1
            mus_id=5401
            mus_name="西藏博物馆"

            item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                                  mus_name=mus_name, col_picture=col_picture)
            yield item

        next_url="http://39.106.176.234//api/exhibit/exhibit_list?p=w&language=1&skip=0&take=6&class="+str(self.classid)
        self.classid+=1
        if self.classid>10:
            return
        else:
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)


