import scrapy

#22 02
from ..items import CollectionItem


class JlmuseumSpider(scrapy.Spider):
    name = 'JLMuseum'
    allowed_domains = ['http://www.jlmuseum.org/']
    start_urls = ['http://www.jlmuseum.org/collection/']

    custom_settings = {
        'ITEM_PIPELINES':{'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    base_url="http://www.jlmuseum.org/"
    flag=0
    Id=10001
    def parse(self, response):
        list=response.xpath("//div[@class='list-pics']/ul/li")
        final_url=response.xpath("//div[@class='pages']/a[last()]/@href").get()
        for li in list:
            col_name=li.xpath(".//div[@class='info']/a/text()").get()
            col_picture=li.xpath(".//div[@class='thumb']/a/img/@src").get()
            col_picture=self.base_url+col_picture
            detail_url=li.xpath(".//div[@class='thumb']/a/@href").get()
            yield scrapy.Request(self.base_url+detail_url,callback=self.prase_detail,dont_filter=True,meta={'col_name':col_name,'col_picture':col_picture})
        next_url=response.xpath("//div[@class='pages']/a[last()-1]/@href").get()
        if self.flag==1:
            return
        if next_url==final_url:
            self.flag=1
        yield scrapy.Request(self.base_url+next_url,callback=self.parse,dont_filter=True)

    def prase_detail(self,response):
        col_name=response.meta['col_name']
        col_picture=response.meta['col_picture']
        col_info=response.xpath("//div[@class='pics-cont']/p[2]//text()").getall()
        col_info="".join(col_info).strip()
        col_era="无或者在info中"
        mus_name="吉林省博物院"
        col_id="2202"+str(self.Id)
        self.Id+=1
        mus_id=2202
        item=CollectionItem(col_id=col_id,mus_id=mus_id,col_name=col_name,col_era=col_era,col_info=col_info,mus_name=mus_name,col_picture=col_picture)
        yield item



