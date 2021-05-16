import scrapy

#4401
from ..items import CollectionItem


class GdmuseumSpider(scrapy.Spider):
    name = 'GDMuseum'
    allowed_domains = ['http://www.gdmuseum.com/']
    start_urls = ['http://www.gdmuseum.com/gdmuseum/_300746/_300758/tc45/index.html']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    #http://www.gdmuseum.com/gdmuseum/_300746/_300810/lddwbb/index.html
    Cr_base_urL="http://www.gdmuseum.com/gdmuseum/_300746/_300758/"
    Ani_base_url="http://www.gdmuseum.com/gdmuseum/_300746/_300810/"
    cr_id=["tc45","sh87","qtq","yq43","jmd50","dy","zx59",""]
    ani_id=["lddwbb","zcybb","bysbb","hydwbb","gswhs","kwbb",""]
    Id=10001
    i=1
    base_url="http://www.gdmuseum.com"
    def parse(self,response):
        start_urls=["http://www.gdmuseum.com/gdmuseum/_300746/_300758/tc45/index.html","http://www.gdmuseum.com/gdmuseum/_300746/_300810/lddwbb/index.html"]
        for j in range(2):
            if j==1:
                yield scrapy.Request(start_urls[j],callback=self.parse_ani,dont_filter=True)
            yield scrapy.Request(start_urls[j],callback=self.parse_cr,dont_filter=True)

    def parse_cr(self, response):
        cont=response.xpath("//div[@class='js_cont']/div")
        for li in cont:
            col_name=li.xpath(".//a[@class='pro_title']/p[@class='name']/text()").get()
            col_picture=li.xpath(".//a[@class='pro_img']/span/img/@src").get()
            col_picture=self.base_url+col_picture
            detail_url = li.xpath(".//a[@class='pro_img']/@href").get()
            yield scrapy.Request(self.base_url + detail_url, callback=self.parse_page1, dont_filter=True,
                                 meta={"col_name": col_name, "col_picture": col_picture})
        next_url=response.xpath("//div[@class='paging']/a[@class='pagingNormal next']/@tagname").get()
        if not next_url:
            next_col=self.Cr_base_urL+self.cr_id[self.i]+'/index.html'
            self.i+=1
            if self.i>7:
                self.i=1
                return
            else:
                yield scrapy.Request(next_col,callback=self.parse_cr,dont_filter=True)
        else:
            yield scrapy.Request(self.base_url+next_url,callback=self.parse_cr,dont_filter=True)



    def parse_page1(self,response):
        col_name = response.meta["col_name"]
        col_picture = response.meta["col_picture"]
        col_info = response.xpath("//div[@class='detail_cont']//text()").getall()
        col_info = ''.join(col_info).strip()
        col_info = ''.join(col_info.split())
        if len(col_info)<7:
            col_info = response.xpath("//div[@class='cp_list']//text()").getall()
            col_info = ''.join(col_info).strip()
            col_info=''.join(col_info.split())
        col_id = "4401"+str(self.Id)
        col_era = "无或在info里"
        mus_name = "广东省博物馆"
        self.Id += 1
        mus_id=4401
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item

    def parse_ani(self,response):
        list=response.xpath("//div[@class='js_cont']/div")
        for li in list:
            col_name=li.xpath(".//a[@class='pro_title']/p[@class='name']/text()").get()
            col_picture = li.xpath(".//a[@class='pro_img']/span/img/@src").get()
            col_picture = self.base_url + col_picture
            detail_url=li.xpath(".//a[@class='pro_img']/@href").get()

            yield scrapy.Request(self.base_url+detail_url,callback=self.parse_page,dont_filter=True,
                                 meta={"col_name":col_name,"col_picture":col_picture})

        next_url = response.xpath("//div[@class='paging']/a[@class='pagingNormal next']/@tagname").get()
        if not next_url:
            next_col=self.Ani_base_url+self.ani_id[self.i]+'/index.html'
            self.i+=1
            if self.i>6:
                self.i=1
                return
            else:
                yield scrapy.Request(next_col,callback=self.parse_ani,dont_filter=True)
        else:
            yield scrapy.Request(self.base_url + next_url, callback=self.parse_ani, dont_filter=True)

    def parse_page(self,response):
        col_name=response.meta["col_name"]
        col_picture=response.meta["col_picture"]
        col_info=response.xpath("//div[@class='cont']//text()").getall()
        col_info=''.join(col_info).strip()
        col_era="无"
        col_id = "4401"+str(self.Id)
        mus_name = "广东省博物馆"
        self.Id += 1
        mus_id=4401
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item
