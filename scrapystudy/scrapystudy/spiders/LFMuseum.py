import scrapy

from ..items import CollectionItem

#1140
class LfmuseumSpider(scrapy.Spider):
    name = 'LFMuseum'
    allowed_domains = ['http://www.linfenmuseum.com/']
    start_urls = ['http://www.linfenmuseum.com/index.php/Index/collection/p1/1']
    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id=10001
    cur_page=1
    base_url="http://www.linfenmuseum.com"
    def parse(self, response):
        list=response.xpath("//div[@class='newslist']/ul/li")
        for li in list:
            col_name=li.xpath(".//a/text()").get()
            detail_url=li.xpath(".//a/@href").get()

            yield scrapy.Request(self.base_url+detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"col_name":col_name})

        next_url=response.xpath("//div[@class='newslist']/div[@class='pages']/a[last()]/@href").get()
        self.cur_page+=1
        if self.cur_page>5:
            return
        else:
            yield scrapy.Request(self.base_url+next_url,callback=self.parse,dont_filter=True)


    def parse_detail(self,response):
        col_name=response.meta["col_name"]
        col_picture=response.xpath("//div[@class='full-left']/a/img/@src").get()
        col_era=response.xpath("//div[@class='title03']/br/preceding-sibling::text()[1]").get()
        col_info=response.xpath("//div[@class='title04']//text()").getall()
        col_info=''.join(col_info).strip()

        col_id="1440"+str(self.Id)
        self.Id+=1
        mus_id=1140

        mus_name='临汾市博物馆'
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item
