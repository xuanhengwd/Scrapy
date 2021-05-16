import scrapy

#3304
from ..items import CollectionItem


class NbmuseumSpider(scrapy.Spider):
    name = 'NBMuseum'
    allowed_domains = ['www.nbmuseum.cn']
    start_urls = ['http://www.nbmuseum.cn/col/col701/index.html']
    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.NjmuseumPipeline': 300}
    }



    Id=10001
    def parse(self, response):
        list=response.xpath("//div[@class='contain']/div")
        for li in list:
            col_name='越窑青瓷'
            col_picture="http://www.nbmuseum.cn/picture/0/s1607280259240264012.jpg"
            col_info=li.xpath(".//text()").getall()
            col_info=''.join(col_info).strip()
            col_id="3304"+str(self.Id)
            self.Id+=1
            mus_id=3304
            col_era="不详"
            mus_name="宁波博物院"
            item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                                  mus_name=mus_name, col_picture=col_picture)
            yield item
