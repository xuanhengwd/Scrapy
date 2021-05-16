import scrapy

from ..items import CollectionItem

#4304
class CsjdmuseumSpider(scrapy.Spider):
    name = 'CSJDMuseum'
    allowed_domains = ['http://www.chinajiandu.cn/']
    start_urls = ['http://www.chinajiandu.cn/Collection/List/wj']


    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    base_url="http://www.chinajiandu.cn"

    col_type=["wj","xhj","dhj","yym",""]
    typeid=1
    Id=10001
    def parse(self, response):
        list=response.xpath("//ul[@class='collectlist ']/li")
        if not list:
            list=response.xpath("//ul[@class='collectlist jianstyle']/li")
        for li in list:
            col_name=li.xpath(".//a/@title").get()
            col_picture=li.xpath(".//a/div/img/@src").get()
            detail_url=li.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_url+detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"col_name":col_name,"col_picture":col_picture})

        next_url="http://www.chinajiandu.cn/Collection/List/"+str(self.col_type[self.typeid])
        self.typeid+=1
        if self.typeid>4:
            return
        else:
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        col_name=response.meta["col_name"]
        col_picture=response.meta["col_picture"]
        col_info=response.xpath("//div[@class='cont']//text()").getall()
        col_info=''.join(col_info).strip()
        col_id="4304"+str(self.Id)
        self.Id+=1
        mus_id=4304
        col_era="无"
        mus_name="长沙简牍博物馆"
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item
