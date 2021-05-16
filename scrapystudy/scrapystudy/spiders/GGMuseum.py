import scrapy


class GgmuseumSpider(scrapy.Spider):
    name = 'GGMuseum'
    allowed_domains = ['https://www.dpm.org.cn/']
    start_urls = ['https://www.dpm.org.cn/explore/collections.html']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    flag=0
    base_url="https://www.dpm.org.cn"
    def parse(self, response):

        box=response.xpath("//div[@class='wrap']/div[@class='box']/div")
        for li in box:
            if self.flag == 1:
                break
            self.flag = 1
            type_url=li.xpath(".//a/@href").get()
            type_url=self.base_url+type_url
            yield scrapy.Request(type_url,callback=self.parse_type,dont_filter=True)



    def parse_type(self,response):
        divs=response.xpath("//div[@id='building2']/div/div[2]/table/tr")
        for tr in divs:
            col_name=tr.xpath(".//td[1]/a/text()").get()
            print(col_name)