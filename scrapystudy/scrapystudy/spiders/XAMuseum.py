import scrapy

##区划码61  musid=6107
from w3lib.html import remove_tags

from ..items import CollectionItem


class XamuseumSpider(scrapy.Spider):
    name = 'XAMuseum'
    allowed_domains = ['https://www.xabwy.com/']
    start_urls = ['https://www.xabwy.com/api/website/article/list?language=0&currentPage=1&pageSize=3&typeId=190']
    typeId=190
    # count=1;
    Id=10001
    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.MuseumPipeline': 300}
    }
    def parse(self, response):
        JsonBody=response.json()
        body=JsonBody["body"]
        totalPage=body["totalPage"]
        # print(totalPage)
        for i in range(int(totalPage)):
            # lists=body["list"]
            # for dect in lists:
            #     id=dect["id"]
            #     print(id)

            next_url='https://www.xabwy.com/api/website/article/list?language=0&currentPage='+str(i+1)+'&pageSize=3&typeId='+str(self.typeId)
            # print("*"*40)
            # print(next_url)
            # print("*" * 40)
            yield scrapy.Request(next_url,callback=self.parse_cur,dont_filter=True)
        self.typeId+=1;
        if self.typeId==198:
            return
        nextex_url='https://www.xabwy.com/api/website/article/list?language=0&currentPage=1&pageSize=3&typeId='+str(self.typeId)
        yield scrapy.Request(nextex_url,callback=self.parse,dont_filter=True)

    def parse_cur(self,reponse):
        Jsonbody=reponse.json()
        body = Jsonbody["body"]
        list=body["list"]
        for dect in list:
            col_picture=dect['litPic']
            id=dect['id']
            detail_url='https://www.xabwy.com/api/website/article/'+str(id)
            yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,meta={'col_picture':col_picture})

    def parse_detail(self,response):

        col_picture=response.meta["col_picture"]
        head=response.json()
        body=head["body"]
        col_name=body["title"]
        col_info=body["body"]
        col_info=remove_tags(col_info)
        col_info=col_info.replace('&nbsp;','').replace('&ldquo;','').replace('&rdquo;','').replace('&hellip;','').strip()
        mus_id=6107
        mus_name="西安博物院"
        col_id="6107"+str(self.Id)
        self.Id+=1
        col_era='在info里或者不存在'
        item=CollectionItem(col_id=col_id,mus_id=mus_id,col_name=col_name,col_era=col_era,col_info=col_info,mus_name=mus_name,col_picture=col_picture)
        yield item
#https://www.xabwy.com/api/website/article/924