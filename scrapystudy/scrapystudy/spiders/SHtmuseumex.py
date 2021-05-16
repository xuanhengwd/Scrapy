import scrapy

#31  04
from ..items import ExhibItem


class ShtmuseumSpider(scrapy.Spider):
    name = 'SHtmuseumex'
    allowed_domains = ['http://www.sstm.org.cn/']
    start_urls = ['http://www.sstm.org.cn/exarea!getList']
    custom_settings = {
        "ITEM_PIPELINES": {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }
    Id=10001
    def parse(self, response):
        url='http://www.sstm.org.cn/exarea!getList'
        #http://www.sstm.org.cn/exarea!getList
        for i in range(2):
            data={
                'type':str(i+1)
            }
            request = scrapy.FormRequest(url,formdata=data,callback=self.parse_detail,dont_filter=True)
            yield request

    def parse_detail(self,response):
        JsonBody=response.json()
        body=JsonBody["body"]
        for dect in body:
            mus_id=3104
            exh_id="3104"+str(self.Id)
            self.Id+=1
            exh_name=dect["title"].strip()
            mus_name="上海科技馆"
            try:
                exh_info=dect['theme']
            except:
                exh_info=dect['title']
            exh_picture=dect['cover']
            try:
                exh_time=dect['startTime']
            except:
                exh_time='无'
                print(exh_name)
            item=ExhibItem(exh_id=exh_id,exh_name=exh_name,mus_id=mus_id,mus_name=mus_name,exh_info=exh_info,exh_picture=exh_picture,exh_time=exh_time)
            yield item
