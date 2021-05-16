import scrapy

from ..items import CollectionItem

#3240
class XuzmuseumSpider(scrapy.Spider):
    name = 'XuZMuseum'
    allowed_domains = ['https://www.xzmuseum.com/']
    start_urls = ['https://www.xzmuseum.com/collection_list.aspx?category_id=594']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }
    Id=10001

    base_url="https://www.xzmuseum.com"
    def parse(self, response):
        list=response.xpath("//div[@class='ny_l']/ul/li")
        num = 0
        for li in list:
            num+=1
            if num>9:
                break
            type_url=li.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_url+type_url,callback=self.parse_type,dont_filter=True)
        #yield scrapy.Request('https://www.xzmuseum.com/collection_list.aspx?category_id=594', callback=self.parse_type, dont_filter=True)


    def parse_type(self,response):
        lists=response.xpath("//ul[@class='dc_list']/li")
        total_page=response.xpath("//div[@class='flickr']/a[last()-1]/text()").get()
        total_page=int(total_page)
        print(total_page)
        for li in lists:
            col_name=li.xpath(".//p/text()").get()
            col_picture=li.xpath(".//a/img/@src").get()
            col_picture=self.base_url+col_picture
            detail_url=li.xpath(".//a/@href").get()
            yield scrapy.Request(self.base_url+detail_url,callback=self.parse_detail,dont_filter=True,
                                 meta={"col_name":col_name,"col_picture":col_picture})

        next_url=response.xpath("//div[@class='flickr']/a[last()]/@href").get()
        cur_page=response.xpath("//div[@class='flickr']/span[@class='current']/text()").get()
        cur_page=int(cur_page)
        if cur_page>total_page:
            return
        else:
            yield scrapy.Request(self.base_url+next_url,callback=self.parse_type,dont_filter=True)


    def parse_detail(self,response):
        col_name=response.meta["col_name"]
        col_picture=response.meta["col_picture"]
        col_era=response.xpath("//div[@class='dc_dr']/p[3]/text()").get()
        col_info=response.xpath("//div[@class='dc_dx']//text()").getall()
        col_info=''.join(col_info).strip()
        col_info=''.join(col_info.split())
        col_id="3240"+str(self.Id)
        self.Id+=1
        mus_id=3240
        mus_name="徐州博物馆"

        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)

        yield item