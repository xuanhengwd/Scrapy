import scrapy
from w3lib.html import remove_tags

from ..items import ExhibItem


class XamuseumexSpider(scrapy.Spider):
    name = 'XAMuseumex'
    allowed_domains = ['https://www.xabwy.com/']
    start_urls = ['https://www.xabwy.com/api/website/article/list?language=0&currentPage=1&pageSize=3&typeId=36']
    cur_page=1
    totalPage=1
    Id=10001
    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.MuseumExPipeline': 300}
    }
    def parse(self, response):
        if self.cur_page>self.totalPage:
            return
        head=response.json()
        body=head["body"]
        self.totalPage=body["totalPage"]
        list=body['list']
        for dect in list:
            exh_picture=dect['litPic']
            id=dect["id"]
            detail_url='https://www.xabwy.com/api/website/article/'+str(id)
            yield scrapy.Request(detail_url,callback=self.prase_detail,dont_filter=True,meta={'exh_picture':exh_picture})
        self.cur_page+=1
        next_url='https://www.xabwy.com/api/website/article/list?language=0&currentPage='+str(self.cur_page)+'&pageSize=3&typeId=36'
        yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)

    def prase_detail(self,response):
        head=response.json()
        body=head["body"]
        exh_picture=response.meta['exh_picture']
        exh_id='6107'+str(self.Id)
        self.Id+=1
        exh_time = body['pubDate']
        exh_name=body['title']
        mus_id=6107
        mus_name="西安博物院"
        exh_info=body['body']
        exh_info=remove_tags(exh_info)
        exh_info=exh_info.replace('&nbsp;', '').replace('&ldquo;','').replace('&middot;','').replace('&rdquo;','').replace('&mdash;','')
        exh_info=exh_info.replace('grave','').replace('grave;','').replace('&','').strip()
        item=ExhibItem(exh_id=exh_id,exh_name=exh_name,mus_id=mus_id,mus_name=mus_name,exh_info=exh_info,exh_picture=exh_picture,exh_time=exh_time)
        yield item
#https://www.xabwy.com/api/website/article/list?language=0&currentPage=1&pageSize=3&typeId=36
#https://www.xabwy.com/api/website/article/list?language=0&currentPage=2&pageSize=3&typeId=36
#https://www.xabwy.com/api/website/article/289
