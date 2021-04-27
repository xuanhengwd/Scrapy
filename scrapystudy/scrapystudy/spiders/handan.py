import json

import scrapy

from ..items import HandanItem


class HandanSpider(scrapy.Spider):
    name = 'handan'
    allowed_domains = ['https://www.hdmuseum.org/']
    start_urls = ['https://www.hdmuseum.org/Product/Query']
    base_url="https://www.hdmuseum.org"

    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.HandanPipleline':300}
    }
    def start_requests(self):
        url = "https://www.hdmuseum.org/Product/Query"
        #三页，懒得去获取页数了。。。
        requests=[]
        for i in range(1, 4):
            data = {
                'classId': '16',
                'pageIndex': str(i),
                'pageSize': '9',
            }
            #请求
            request = scrapy.FormRequest(url, formdata=data, callback=self.parse_page)
            requests.append(request)
            yield request
        #return requests
    def parse_page(self,response):
        #得到响应的json
        jsonBody =response.json()
        # jsonBody=json.loads(response.body.decode('gbk').encode('utf-8'))
        models=jsonBody['list']
        #对json里的逐个返回item
        for dict in models:
            id=dict['id']
            productName=dict['productName']
            img=self.base_url+dict['img']
            description=dict['description']
            item=HandanItem(id=id,productName=productName,img=img,description=description)
            yield item


