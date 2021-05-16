import scrapy

# 2104
from ..items import CollectionItem


class LsmuseumSpider(scrapy.Spider):
    name = 'LSmuseum'
    allowed_domains = ['http://www.lvshunmuseum.org/']
    start_urls = ['http://www.lvshunmuseum.org/collection/product.aspx?SortID=9']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    base_url = "http://www.lvshunmuseum.org"
    SortID = 10
    sort_url = "http://www.lvshunmuseum.org/collection/product.aspx?SortID="

    Id = 10001

    def parse(self, response):

        list = response.xpath(".//div[@class='collection']/ul/li")
        for li in list:
            col_name = li.xpath(".//a/div[@class='textbox textbox2']/h1/text()").get()
            col_picture = li.xpath(".//a/div[@class='picbox']/img/@src").get().strip()
            col_picture = self.base_url + col_picture
            detail_url = li.xpath(".//a/@href").get().strip()
            yield scrapy.Request(self.base_url + detail_url, callback=self.parse_detail, dont_filter=True,
                                 meta={"col_name": col_name, "col_picture": col_picture})
        next_url = response.xpath("//div[@class='pagination']/a[last()]/@href").get()
        if next_url == "javascript:;":
            request = scrapy.Request(self.sort_url + str(self.SortID), callback=self.parse, dont_filter=True)
            self.SortID += 1
            if self.SortID > 18:
                return
            else:
                yield request
        else:
            yield scrapy.Request(self.base_url + next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        col_name = response.meta["col_name"]
        col_picture = response.meta["col_picture"]
        col_info = response.xpath("//div[@class='textshow']//text()").getall()
        col_info = "".join(col_info).strip()
        col_info=''.join(col_info.split())
        col_id = "2104" + str(self.Id)
        self.Id += 1
        mus_id = 2104
        col_era = "在name里"
        mus_name = "旅顺博物馆"
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)
        yield item
