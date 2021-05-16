import scrapy

#三星堆博物馆
#51 02
from ..items import CollectionItem


class SxdmuseumSpider(scrapy.Spider):
    name = 'SXDMuseum'
    allowed_domains = ['http://www.sxd.cn']
    start_urls = ['http://www.sxd.cn/list_2.asp?bigclass=29&smallclass=4']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id=10001
    classid=1
    typeid=["4","5","6","43",""]
    base_url="http://www.sxd.cn/"
    def parse(self, response):
        trs=response.xpath("/html/body/div[1]/div[2]/div[2]/table[2]/tr/td[2]/table/tr[2]/td/table/tr/td/table[1]/tr")
        for tr in trs:
            tds=tr.xpath(".//td")
            for td in tds:
                col_picture=td.xpath(".//div[@class='picout']/div/a/img/@src").get()
                col_name=td.xpath(".//div[2]/font/text()").get()
                if not col_name:
                    break
                col_picture = self.base_url + col_picture
                col_name=col_name.strip()

                detail = td.xpath(".//div[@class='picout']/div/a/@href").get()
                detail_id=filter(str.isdigit, detail)
                detail_id=''.join(detail_id)
                detail_url="http://www.sxd.cn/showinfojp.asp?id="+detail_id
                yield scrapy.Request(detail_url,callback=self.parse_detail,dont_filter=True,
                                     meta={"col_name":col_name,"col_picture":col_picture})
        find=response.xpath("/html/body/div[1]/div[2]/div[2]/table[2]/tr/td[2]/table/tr[2]/td/table/tr/td/table[1]")
        next_url=find.xpath(".//tr[last()]/table/tr[1]/td/table/tr/td/a[3]/@href").get()
        last_url=find.xpath(".//tr[last()]/table/tr[1]/td/table/tr/td/a[4]/@href").get()
        if next_url[14:16]>last_url[14:16]:
            url="http://www.sxd.cn/list_2.asp?bigclass=29&smallclass="+self.typeid[self.classid]
            self.classid+=1
            if self.classid>4:
                return
            yield scrapy.Request(url,callback=self.parse,dont_filter=True)


        else:
            next_url="http://www.sxd.cn/list_2.asp"+next_url
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)


    def parse_detail(self,response):
        col_name=response.meta["col_name"]
        col_picture=response.meta["col_picture"]
        col_info=response.xpath("//table/tr/td/table/tr[2]/td//text()").getall()
        col_info="".join(col_info).strip()
        col_era="不详"
        col_id="5102"+str(self.Id)
        self.Id+=1
        mus_id=5102
        mus_name="三星堆博物馆"
        item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                              mus_name=mus_name, col_picture=col_picture)

        yield item


