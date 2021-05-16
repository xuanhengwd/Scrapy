import scrapy
from w3lib.html import remove_tags

# 1109
from ..items import CollectionItem


class A1937cmuseumSpider(scrapy.Spider):
    name = '1937Cmuseum'
    allowed_domains = ['http://www.1937china.com/']
    start_urls = ['http://www.1937china.com/']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id = 10001
    base_url = "http://www.1937china.com/kzgdata/image/thumbnail/"
    def parse(self, response):
        url1 = 'http://www.1937china.com/rest/business/kzslw/kzwwJpdc/list'
        for i in range(12):
            data = {
                'status': '0',
                'pageSize': '10',
                'pageNum': str(i + 1),
            }
            request = scrapy.FormRequest(url1, formdata=data, callback=self.parse_detail, dont_filter=True)
            yield request
        url2 = 'http://www.1937china.com/rest/business/kzslw/kzwwShjx/list'
        for i in range(6):
            data = {
                'status': '0',
                'pageSize': '12',
                'pageNum': str(i + 1),

            }
            request = scrapy.FormRequest(url2, formdata=data, callback=self.parse_detail1, dont_filter=True)
            yield request

    def parse_detail(self, response):
        total = response.json()
        rows = total["rows"]
        for dect in rows:
            col_name = dect['title']
            col_era = '无'
            col_info = dect['content']
            col_info = ''.join(col_info).strip()
            col_info = remove_tags(col_info)
            col_info = col_info.replace('&nbsp;', " ")
            mus_name = "国人民抗日战争纪念馆"
            col_picture = dect["image"]
            col_picture = self.base_url + col_picture
            col_id = "1109" + str(self.Id)
            self.Id += 1
            mus_id = 1109
            item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                                  mus_name=mus_name, col_picture=col_picture)
            yield item

    def parse_detail1(self, response):
        total = response.json()
        rows = total["rows"]
        for dect in rows:
            col_name = dect['title']
            col_era = '无'
            col_info = "无"
            mus_name = "国人民抗日战争纪念馆"
            col_picture = dect["image"]
            col_picture = self.base_url + col_picture
            col_id = "1109" + str(self.Id)
            self.Id += 1
            mus_id = 1109
            item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                                  mus_name=mus_name, col_picture=col_picture)
            yield item
