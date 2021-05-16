import scrapy

from ..items import ExhibItem


class A1937cmuseumexSpider(scrapy.Spider):
    name = '1937Cmuseumex'
    allowed_domains = ['http://www.1937china.com/']
    start_urls = ['http://www.1937china.com/']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    base_url="http://www.1937china.com"
    img_url="http://www.1937china.com/kzgdata/image/original/"
    Id=10001
    def parse(self, response):
        url = "http://www.1937china.com/rest/business/kzslw/kzzlZtzl/list"
        data = {
            'status': '0',
            'isColRec': '0',
            'releasePlace': '2'
        }
        request = scrapy.FormRequest(url, formdata=data, callback=self.parse_detail, dont_filter=True)
        yield request

    def parse_detail(self, response):
        total=response.json()
        rows=total["rows"]
        for dect in rows:
            exh_id="1109"+str(self.Id)
            self.Id+=1
            exh_name=dect["title"]
            mus_id=1109
            mus_name="中国人民抗日战争纪念馆"
            exh_info=dect["simpleDescribe"]
            exh_picture=dect["image"]
            exh_picture=self.img_url+exh_picture
            exh_time="无"
            item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                             exh_picture=exh_picture, exh_time=exh_time)
            yield item


