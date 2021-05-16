import scrapy


# 3706
from ..items import CollectionItem


class YtmuseumSpider(scrapy.Spider):
    name = 'YTmuseum'
    allowed_domains = ['http://www.ytmuseum.com/']
    start_urls = ['http://www.ytmuseum.com/collection/zg']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id = 10001
    c_id = ["zg", "cq", "qtq", "yq", "zh", "ww", "gmww", "qt"]
    base_url = "http://www.ytmuseum.com"

    def parse(self, response):
        # list=response.xpath("//div[@class='InLine']/ul/li")
        # for li in list:
        #     col_id=self.Id
        #     print(col_id)
        #     self.Id+=1
        #     col_name=li.xpath(".//div[@class='dclist1']/span/text()").get()
        #     col_era="无"
        #     col_info=li.xpath(".//div[@class='dclist2']/div[@class='dclist2nr']//text()").getall()
        #     col_info="".join(col_info).strip()
        #     col_picture=li.xpath(".//div[@class='dclist2']/div[@class='dclist2img']/a/img/@src").get()
        #     col_picture=col_picture.replace("//","")
        #     print(col_name)
        # next_url=response.xpath("//ul[@class='pagination']/li[last()-1]/a/@href").get()
        # if not next_url:
        for i in range(8):
            next_list_url = "http://www.ytmuseum.com/collection/" + self.c_id[i]
            yield scrapy.Request(next_list_url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        list = response.xpath("//div[@class='InLine']/ul/li")
        for li in list:
            col_id = "3706" + str(self.Id)
            self.Id += 1
            mus_id = 3706
            mus_name = "烟台市博物馆"
            col_name = li.xpath(".//div[@class='dclist1']/span/text()").get()
            col_era = "info里或不详"
            col_info = li.xpath(".//div[@class='dclist2']/div[@class='dclist2nr']//text()").getall()
            col_info = "".join(col_info).strip()
            col_picture = li.xpath(".//div[@class='dclist2']/div[@class='dclist2img']/a/img/@src").get()
            col_picture = col_picture.replace("//", "")
            item=CollectionItem(col_id=col_id,mus_id=mus_id,col_name=col_name,col_era=col_era,col_info=col_info,mus_name=mus_name,col_picture=col_picture)
            yield item

        next_url = response.xpath("//ul[@class='pagination']/li[last()-1]/a/@href").get()
        if not next_url:
            return
        yield scrapy.Request(self.base_url + next_url, callback=self.parse_detail, dont_filter=True)
