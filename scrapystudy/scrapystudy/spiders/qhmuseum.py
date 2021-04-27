import scrapy

from ..items import CollectionItem


#行政区划代码63
#博物馆编码6301
#藏品编码6301+五位
class QhmuseumSpider(scrapy.Spider):
    name = 'qhmuseum'
    allowed_domains = ['qhmuseum.cn']
    start_urls = ['http://www.qhmuseum.cn/qhm-webapi/api/v1/collection/getTextureAll?pageNumber=1&pageSize=10&texture=104']
    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.QhmuseumPipeline':300}
    }
    base_url = "http://www.qhmuseum.cn/qhm-webapi/api/v1/collection/getTextureAll?"
    pagenum = 1;
    texture = ["104", "101", "102", "103", "111", "110", "106", "112"]
    i = 1
    Id = 10001

    def parse(self, response):
        jsonBody = response.json()
        data = jsonBody['data']
        list = data["list"]
        for dict in list:
            col_id="6031"+str(self.Id)
            self.Id+=1
            mus_id=6301
            col_name=dict["collectionname"]
            col_era=dict["category"]
            col_info=dict["collectiondescribe"]
            mus_name="青海省博物馆"
            col_picture=dict["collectionimages"]
            item = CollectionItem(col_id=col_id,mus_id=mus_id,col_name=col_name,col_era=col_era,col_info=col_info,mus_name=mus_name,col_picture=col_picture)
            yield item

        self.pagenum = self.pagenum + 1
        count = int(data['pages'])
        if self.pagenum <= count:
            pnum = str(self.pagenum)
            next_url = self.base_url + "pageNumber=" + pnum + "&pageSize=10&texture=" + self.texture[self.i - 1]
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
        else:
            self.pagenum = 1
            if self.i > 7:
                return
            new_url = self.base_url + "pageNumber=1&pageSize=10&texture=" + self.texture[self.i]
            self.i += 1
            yield scrapy.Request(new_url, callback=self.parse, dont_filter=True)

