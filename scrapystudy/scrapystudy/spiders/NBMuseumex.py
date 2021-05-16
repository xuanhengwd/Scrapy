import scrapy


class NbmuseumexSpider(scrapy.Spider):
    name = 'NBMuseumex'
    allowed_domains = ['www.nbmuseum.cn']
    start_urls = ['http://www.nbmuseum.cn/col/col461/index.html?uid=1730&pageNum=1']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    def parse(self, response):
        content = response.xpath("//div[@id='content']/div[2]/div[2]/div/script").get()
        text = content.replace("<![CDATA[", "").replace("]]>", "").replace("<record>", "").replace("</record>",
                                                                                                   "").replace(
            "<datastore>", "").replace("</datastore>","").replace("<recordset>","").replace("</recordset>","")
        sel = scrapy.Selector(text=text)
        list = sel.xpath("//script/tr").get()
        print(list)

    def parse_detial(self, response):
        pass
