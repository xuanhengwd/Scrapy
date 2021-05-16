import re

import scrapy

from ..items import ExhibItem


class HbmuseumexSpider(scrapy.Spider):
    name = 'HBMuseumex'
    allowed_domains = ['http://www.hbww.org/home/Index.aspx']
    start_urls = ['http://www.hbww.org/ashx/ajax.ashx?type=Archives&channelNo=LSZL']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumExPipeline': 300}
    }

    Id = 10001
    page_id = 2

    def parse(self, response):
        Body = response.json()
        page_count = Body["PageCount"]
        rows = Body["Rows"]
        for dect in rows:
            exh_name = dect["Title"]

            exh_id = "4201" + str(self.Id)
            self.Id += 1
            mus_id = 4201
            mus_name = "湖北省博物馆"
            exh_info = dect["Contents"]
            exh_info =re.sub("[A-Za-z\;\&]", "", exh_info).strip()

            exh_picture=dect["ThumImg"]
            exh_picture="http://file.hbww.org/ThumbCover/" + exh_picture
            exh_time="临时展览"
            print(exh_info)
            item = ExhibItem(exh_id=exh_id, exh_name=exh_name, mus_id=mus_id, mus_name=mus_name, exh_info=exh_info,
                             exh_picture=exh_picture, exh_time=exh_time)
            yield item
        next_url = "http://www.hbww.org/ashx/ajax.ashx?type=Archives&channelNo=LSZL" + "&page=" + str(self.page_id)
        self.page_id += 1
        if self.page_id > page_count + 1:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True, )
