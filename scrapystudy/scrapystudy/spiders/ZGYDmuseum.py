import scrapy


# 3103
from ..items import CollectionItem


class ZgydmuseumSpider(scrapy.Spider):
    name = 'ZGYDmuseum'
    allowed_domains = ['http://www.zgyd1921.com/']
    start_urls = ['http://www.zgyd1921.com/zgyd/node3/n17/n18/index.html']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id = 10001
    base_url = "http://www.zgyd1921.com"
    nid=19
    def parse(self, response):
        list = response.xpath("//ul[@class='piclist2']/li")
        for li in list:
            col_picture = li.xpath(".//a/img/@src").get()
            col_picture = self.base_url + col_picture
            col_name=li.xpath(".//p/a/text()").get()
            url = li.xpath(".//a/@href").get()
            url = self.base_url + url
            yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True, meta={"col_picture": col_picture,"col_name":col_name})
        next_url = response.xpath("//div[@id='AspNetPager1']/a[last()]/@href").get()
        if not next_url:
            return
            # next_col_url="http://www.zgyd1921.com/zgyd/node3/n17/n"+str(self.nid)+"/index.html"
            # self.nid+=1
            # if self.nid>21:
            #     return
            # else:
            #     yield scrapy.Request(next_col_url,callback=self.parse,dont_filter=True)
        else:
            yield scrapy.Request(self.base_url + next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        content = response.xpath("//div[@class='grey14 lh30']//text()").getall()
        content = ''.join(content).strip()
        content=content.split('\n')
        col_info=''.join(content[-1]).strip()
        col_name =response.meta["col_name"]
        col_era = ''.join(content[2]).strip()
        if col_era[0]!="年":
            col_era = ''.join(content[3]).strip()
        col_id = "3103" + str(self.Id)
        mus_id = 3103
        self.Id += 1
        mus_name="中共一大会址纪念馆"
        col_picture=response.meta["col_picture"]
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item
