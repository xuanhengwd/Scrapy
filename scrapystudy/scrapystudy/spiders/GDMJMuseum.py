import scrapy
from w3lib.html import remove_tags

from ..items import CollectionItem

#4406
class GdmjmuseumSpider(scrapy.Spider):
    name = 'GDMJMuseum'
    allowed_domains = ['https://www.gzchenjiaci.com/']
    start_urls = ['https://www.gzchenjiaci.com/MYwebsite/rc/my_cpfl.htm']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    type=["彩瓷","潮州刺绣","漆","木雕","枫溪瓷器","广东剪纸","广东石雕","广彩","广绣","黑瓷白瓷",
          "珐琅","麦秆贴画","墨","木板年画","青瓷","石湾陶","蚀花玻璃","铜镜","象牙雕","椰榄雕","玉雕","竹雕",""]
    base_url="https://www.gzchenjiaci.com/MYwebsite"
    Id=10001

    def parse(self, response):
        url = "https://www.gzchenjiaci.com/MYwebsite/rc/CollectionBoutique"
        for i in range(22):
            data={
                "page":"1",
                "size":"3",
                "articletype":"4",
                "auditstatus":"2",
                "texture":self.type[i],
                "title":""
            }
            yield scrapy.FormRequest(url,formdata=data,callback=self.parse_detail,dont_filter=True,meta={"typei":i})

    def parse_detail(self,response):
        url = "https://www.gzchenjiaci.com/MYwebsite/rc/CollectionBoutique"
        typei=response.meta["typei"]
        Body=response.json()
        count=Body["count"]

        page_count=int(count/3)
        if count%3!=0:
            page_count+=1

        for i in range(page_count):
            data={
                "page":str(i+1),
                "size":"3",
                "articletype":"4",
                "auditstatus":"2",
                "texture":self.type[typei],
                "title":""
            }
            yield scrapy.FormRequest(url, formdata=data, callback=self.parse_details, dont_filter=True,)

    def parse_details(self,response):
        Body = response.json()
        data = Body["data"]
        for dect in data:
            col_name = dect["title"]
            col_picture = dect["imgurl"].strip()
            col_picture = self.base_url + col_picture
            col_era = dect["age"]
            if col_era == "":
                col_era = "不详"
            col_info = dect["content"]
            col_info = remove_tags(col_info).replace("&nbsp;", "").strip()
            mus_name = "广东民间工艺博物馆"
            mus_id = 4406
            col_id = '4406' + str(self.Id)
            self.Id += 1
            item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                                  mus_name=mus_name, col_picture=col_picture)
            yield item