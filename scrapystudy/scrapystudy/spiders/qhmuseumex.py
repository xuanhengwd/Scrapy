import scrapy
from w3lib.html import remove_tags

from ..items import ExhibItem
import re

class QhmuseumexSpider(scrapy.Spider):
    name = 'qhmuseumex'
    allowed_domains = ['qhmuseum.cn']
    start_urls = ['http://www.qhmuseum.cn/qhm-webapi/api/v1/permanent/permanentAll?pageNumber=1&pageSize=10']
    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.QhmuseumexPipeline':300}
    }
    Id = 10001
    def parse(self, response):
        JsonBody=response.json()
        data=JsonBody["data"]
        list=data["list"]
        total=int(data["total"])
        items=[]
        for dict in list:
            exh_id="6301"+str(self.Id)
            self.Id+=1
            mus_id=6031
            exh_name=dict["title"]
            exh_info=dict["contents"]
            exh_info=remove_tags(exh_info)
            mus_name="青海省博物馆"
            exh_pictures=dict["images"]
            #exh_picture=exh_picture[0:exh_picture.rfind('/#')]
            exh_picture=""
            if exh_pictures is not None:
                for i in range(len(exh_pictures)):
                    if exh_pictures[i]!="#":
                        exh_picture+=exh_pictures[i]
                    else:break
            exh_time=dict["createtime"]
            item=ExhibItem(exh_id=exh_id,mus_id=mus_id,exh_name=exh_name,exh_info=exh_info,mus_name=mus_name,exh_picture=exh_picture,exh_time=exh_time)
            items.append(item)
        return items


