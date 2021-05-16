import scrapy
from w3lib.html import remove_tags

from ..items import CollectionItem


# 4201
class HbmuseumSpider(scrapy.Spider):
    name = 'HBMuseum'
    allowed_domains = ['http://www.hbww.org/home/Index.aspx']
    start_urls = ['http://www.hbww.org/ashx/ajax.ashx?type=Archives&channelNo=GZZQ']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapystudy.pipelines.MuseumPipeline': 300}
    }

    Id = 10001
    page_id = 2
    base_url = 'http://www.hbww.org/ashx/ajax.ashx?type=Archives&channelNo='
    col_type = ["GZZQ", "QT", "CQMQ", "JYQ", "ZJ", "YQ", "TCQ", "SH"]

    def parse(self, response):
        for i in range(8):
            detail_url = 'http://www.hbww.org/ashx/ajax.ashx?type=Archives&channelNo=' + self.col_type[i]
            yield scrapy.Request(detail_url, callback=self.parse_detail, dont_filter=True, meta={"typeid": i})
        # detail_url = 'http://www.hbww.org/ashx/ajax.ashx?type=Archives&channelNo=' + self.col_type[3]
        # yield scrapy.Request(detail_url, callback=self.parse_detail, dont_filter=True, meta={"typeid": 3})

    def parse_detail(self, response):
        typeid = int(response.meta["typeid"])
        Body = response.json()
        PageCount = Body["PageCount"]
        print(str(typeid) + ":" + str(PageCount))
        rows = Body["Rows"]
        for dect in rows:
            col_name = dect["Title"]
            col_era = "不详或在描述里"
            col_info = dect["Contents"]
            col_info = col_info.replace("&lt;", "").replace("p&gt;", "").replace("&kh;", "").replace("span",
                                                                                                     "").replace("&dd;",
                                                                                                                 "")
            col_info = col_info.replace("&gg;", "").replace("&gt;", "").replace("&nbsp;", " ").replace("&lf;",
                                                                                                       "").replace(
                "style=line-height:15;", "")
            col_info = col_info.replace("br", "").replace("pstyle=text-align:center;", "").replace(
                "pclass=MsoNormalalign=centerstyle=text-align:left;", "").replace("Golddusted", "").strip()
            col_picture = dect["ThumImg"].strip()
            col_picture = "http://file.hbww.org/ThumbCover/" + col_picture
            col_id = '4201' + str(self.Id)
            self.Id += 1
            mus_id = 4201
            mus_name = '湖北省博物馆'
            item = CollectionItem(col_id=col_id, mus_id=mus_id, col_name=col_name, col_era=col_era, col_info=col_info,
                                  mus_name=mus_name, col_picture=col_picture)
            yield item
        # 翻页
        next_url = self.base_url + self.col_type[typeid] + "&page=" + str(self.page_id)
        self.page_id += 1
        if self.page_id > PageCount + 1:
            self.page_id = 2
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse_detail, dont_filter=True, meta={"typeid": typeid})


{'Rows': [{'Row': 1, 'RowNum': 124, 'ID': 3888, 'Guid': '00a0fb99-f10b-4e8f-abdd-1436588504f4', 'Flag': '',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '铜鼎', 'TitleColor': '', 'Tag': '', 'Source': '',
           'VisitCount': 184, 'Description': '',
           'Contents': '战国中晚期（距今约2320年），九连墩1号幕出土，盛熟牲鼎，通高32&dd;7，口径25&dd;4，腹径30，两耳间距33&dd;4cm', 'IsPublish': 1,
           'CreateDate': '2016-05-07T14:33:41.663', 'UpdateDate': '2016-05-07T14:33:41.663',
           'PublishDate': '2016-05-07T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': None,
           'Column3': None, 'ThumImg': '文章管理缩略图/20160507023328cZ4SWp.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': '', 'IsComment': False, 'IsCreateHTML': None, 'Page': 0, 'ChannelNo': 'QT',
           'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b', 'ParentChannelNo': 'Collection',
           'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0},
          {'Row': 2, 'RowNum': 187, 'ID': 3516, 'Guid': '01b2e8b3-70b0-43f9-b8c9-b9fee1ab672e', 'Flag': '',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '嵌红铜几何纹龙形足铜敦', 'TitleColor': '', 'Tag': '',
           'Source': '', 'VisitCount': 381, 'Description': '',
           'Contents': '&lt;p&gt;&kh;&nbsp;&kh;&lt;&lf;p&gt;&kh;&lt;p&gt;&kh;战国，高27,口径21&dd;5cm，1973年襄阳蔡坡4号墓出土。&kh;&lt;&lf;p&gt;',
           'IsPublish': 1, 'CreateDate': '2016-03-01T20:19:10', 'UpdateDate': '2016-03-13T15:14:05.953',
           'PublishDate': '2016-03-01T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': None,
           'Column3': None, 'ThumImg': '文章管理缩略图/20160301081908ZLAF5D.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': '', 'IsComment': False, 'IsCreateHTML': None, 'Page': 0, 'ChannelNo': 'QT',
           'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b', 'ParentChannelNo': 'Collection',
           'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0},
          {'Row': 3, 'RowNum': 11, 'ID': 5042, 'Guid': '0360981c-b290-4fa8-8675-c3ef288852cc', 'Flag': '',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '镶嵌龙凤纹樽', 'TitleColor': '', 'Tag': '',
           'Source': '', 'VisitCount': 1392, 'Description': '', 'Contents': '高17,口径24&dd;5cm,江陵望山M2头箱', 'IsPublish': 1,
           'CreateDate': '2018-05-22T16:41:05.383', 'UpdateDate': '2018-05-22T16:41:05.383',
           'PublishDate': '2018-05-22T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': '',
           'Column3': None, 'ThumImg': '文章管理缩略图/20180522044027l9Fmd3.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': 'http://file.hbww.org/threed/5.566.html', 'IsComment': False, 'IsCreateHTML': None, 'Page': None,
           'ChannelNo': 'QT', 'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b',
           'ParentChannelNo': 'Collection', 'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0},
          {'Row': 4, 'RowNum': 159, 'ID': 3923, 'Guid': '04375914-eb4a-474b-8d57-9a0884ab9637', 'Flag': '',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '寒公孙爿訁父铜匜', 'TitleColor': '', 'Tag': '',
           'Source': '', 'VisitCount': 453, 'Description': '', 'Contents': '春秋，宽14&dd;5cm，1965年枝江百里洲出土', 'IsPublish': 1,
           'CreateDate': '2016-05-07T15:01:08.06', 'UpdateDate': '2016-05-07T15:01:08.06',
           'PublishDate': '2016-05-07T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': None,
           'Column3': None, 'ThumImg': '文章管理缩略图/20160507030049AnVGbc.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': '', 'IsComment': False, 'IsCreateHTML': None, 'Page': 0, 'ChannelNo': 'QT',
           'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b', 'ParentChannelNo': 'Collection',
           'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0},
          {'Row': 5, 'RowNum': 116, 'ID': 3880, 'Guid': '05bfec6f-1192-4514-b6af-0fb5eae144c3', 'Flag': '',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '铜卵缶', 'TitleColor': '', 'Tag': '', 'Source': '',
           'VisitCount': 203, 'Description': '', 'Contents': '战国，高34，口径21，耳距45cm，1986年荆门包山2号墓出土', 'IsPublish': 1,
           'CreateDate': '2016-05-07T14:25:00', 'UpdateDate': '2018-05-22T17:55:09.637',
           'PublishDate': '2016-05-07T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': '',
           'Column3': None, 'ThumImg': '文章管理缩略图/20160507022448Yj0UO9.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': 'http://file.hbww.org/threed/5.1955.html', 'IsComment': False, 'IsCreateHTML': None, 'Page': 0,
           'ChannelNo': 'QT', 'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b',
           'ParentChannelNo': 'Collection', 'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0},
          {'Row': 6, 'RowNum': 6, 'ID': 5058, 'Guid': '0628bc34-c97d-4701-a365-be37df2710e4', 'Flag': '',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '窃曲纹铜盘', 'TitleColor': '', 'Tag': '',
           'Source': '', 'VisitCount': 1231, 'Description': '', 'Contents': '高16&dd;1，口径41&dd;3cm，京山苏家垅',
           'IsPublish': 1, 'CreateDate': '2018-05-24T10:39:13.417', 'UpdateDate': '2018-05-24T10:39:13.417',
           'PublishDate': '2018-05-24T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': '',
           'Column3': None, 'ThumImg': '文章管理缩略图/201805241039044MH6V5.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': 'http://file.hbww.org/threed/5.3527.html', 'IsComment': False, 'IsCreateHTML': None, 'Page': None,
           'ChannelNo': 'QT', 'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b',
           'ParentChannelNo': 'Collection', 'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0},
          {'Row': 7, 'RowNum': 172, 'ID': 3469, 'Guid': '06d51b7f-2f53-40ae-9136-1abafedeba7a', 'Flag': '',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '曾仲斿父壶', 'TitleColor': '', 'Tag': '',
           'Source': '', 'VisitCount': 627, 'Description': '',
           'Contents': '&lt;p&gt;&kh;&lt;span&kh;style=&gg;font-family:宋体;font-size:10&dd;5pt;mso-bidi-font-size:10&dd;0pt;&gg;&gt;&lt;&lf;span&gt;&nbsp;&kh;&lt;&lf;p&gt;&kh;&lt;p&gt;&kh;&lt;span&kh;style=&gg;font-family:宋体;font-size:10&dd;5pt;mso-bidi-font-size:10&dd;0pt;&gg;&gt;西周晚期，通高&lt;&lf;span&gt;&lt;span&kh;lang=&gg;EN-US&gg;&kh;style=&gg;font-family:&quot;font-size:10&dd;5pt;mso-bidi-font-size:10&dd;0pt;mso-font-kerning:1&dd;0pt;mso-ansi-language:EN-US;mso-fareast-language:ZH-CN;mso-bidi-language:AR-SA;mso-fareast-font-family:宋体;&gg;&gt;66&lt;&lf;span&gt;&lt;span&kh;style=&gg;font-family:宋体;font-size:10&dd;5pt;mso-bidi-font-size:10&dd;0pt;&gg;&gt;，宽&lt;&lf;span&gt;&lt;span&kh;lang=&gg;EN-US&gg;&kh;style=&gg;font-family:&quot;font-size:10&dd;5pt;mso-bidi-font-size:10&dd;0pt;mso-font-kerning:1&dd;0pt;mso-ansi-language:EN-US;mso-fareast-language:ZH-CN;mso-bidi-language:AR-SA;mso-fareast-font-family:宋体;&gg;&gt;23&dd;8cm&lt;&lf;span&gt;&lt;span&kh;style=&gg;font-family:宋体;font-size:10&dd;5pt;mso-bidi-font-size:10&dd;0pt;&gg;&gt;，&lt;&lf;span&gt;&lt;span&kh;lang=&gg;EN-US&gg;&kh;style=&gg;font-family:&quot;font-size:10&dd;5pt;mso-bidi-font-size:10&dd;0pt;mso-font-kerning:1&dd;0pt;mso-ansi-language:EN-US;mso-fareast-language:ZH-CN;mso-bidi-language:AR-SA;mso-fareast-font-family:宋体;&gg;&gt;1996&lt;&lf;span&gt;&lt;span&kh;style=&gg;font-family:宋体;font-size:10&dd;5pt;mso-bidi-font-size:10&dd;0pt;&gg;&gt;年湖北京山宋河坪坝苏家垅出土。&lt;&lf;span&gt;&kh;&lt;&lf;p&gt;',
           'IsPublish': 1, 'CreateDate': '2016-03-01T19:28:40', 'UpdateDate': '2016-03-13T15:07:28.327',
           'PublishDate': '2016-03-01T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': None,
           'Column3': None, 'ThumImg': '文章管理缩略图/20160301073039HrCRqw.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': '', 'IsComment': False, 'IsCreateHTML': None, 'Page': 0, 'ChannelNo': 'QT',
           'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b', 'ParentChannelNo': 'Collection',
           'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0},
          {'Row': 8, 'RowNum': 182, 'ID': 3502, 'Guid': '09a6449a-8044-41af-a9fc-228eccc476be', 'Flag': 'c',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '楚屈子赤角簠', 'TitleColor': '', 'Tag': '',
           'Source': '', 'VisitCount': 452, 'Description': '',
           'Contents': '&lt;p&gt;&kh;&nbsp;&kh;&lt;&lf;p&gt;&kh;&lt;p&gt;&kh;春秋，长27&dd;7，宽20&dd;7cm，1975年随州鲢鱼嘴出土。&kh;&lt;&lf;p&gt;',
           'IsPublish': 1, 'CreateDate': '2016-03-01T20:12:19', 'UpdateDate': '2018-05-22T15:50:39.813',
           'PublishDate': '2016-03-01T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': '',
           'Column3': None, 'ThumImg': '文章管理缩略图/20160301081217Y01UIG.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': '', 'IsComment': False, 'IsCreateHTML': None, 'Page': 0, 'ChannelNo': 'QT',
           'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b', 'ParentChannelNo': 'Collection',
           'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0},
          {'Row': 9, 'RowNum': 10, 'ID': 5041, 'Guid': '0a30deb5-e3f8-465f-9da1-852077604ae2', 'Flag': '',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '蟠螭纹龙形耳铜和', 'TitleColor': '', 'Tag': '',
           'Source': '', 'VisitCount': 712, 'Description': '',
           'Contents': '口径长11&dd;9，口径宽9&dd;7，耳距13&dd;5，高5&dd;3cm，襄阳余岗山湾采集:12', 'IsPublish': 1,
           'CreateDate': '2018-05-22T15:43:52.073', 'UpdateDate': '2018-05-22T15:43:52.073',
           'PublishDate': '2018-05-22T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': '',
           'Column3': None, 'ThumImg': '文章管理缩略图/20180522034313k0MJma.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': 'http://file.hbww.org/threed/5.556.html', 'IsComment': False, 'IsCreateHTML': None, 'Page': None,
           'ChannelNo': 'QT', 'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b',
           'ParentChannelNo': 'Collection', 'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0},
          {'Row': 10, 'RowNum': 27, 'ID': 4312, 'Guid': '0b13e856-cba7-4cb8-9424-0af27602bfd6', 'Flag': '',
           'Channel': 'c54b5946-8028-4d1a-9d88-64bee7ef9969', 'Title': '铜锛', 'TitleColor': '', 'Tag': '', 'Source': '',
           'VisitCount': 207, 'Description': '',
           'Contents': '&lt;p&gt;&kh;楼子湾1号墓出土&kh;&lt;&lf;p&gt;&kh;&lt;p&gt;&kh;长18&dd;7、刃宽3&dd;2cm&kh;&lt;&lf;p&gt;&kh;&lt;p&gt;&kh;盘龙城遗址中发现青铜工具和农具有锛、锄、斫、铲、凿等20余种，多数为实用器物。&kh;&lt;&lf;p&gt;&kh;&lt;p&gt;&kh;&lt;br&kh;&lf;&gt;&kh;&lt;&lf;p&gt;',
           'IsPublish': 1, 'CreateDate': '2016-05-21T16:19:25.937', 'UpdateDate': '2016-05-21T16:19:25.937',
           'PublishDate': '2016-05-21T00:00:00', 'FileIndex': '', 'ShowFileIndex': '0', 'Column1': '', 'Column2': None,
           'Column3': None, 'ThumImg': '文章管理缩略图/20160521041917GlnylB.jpg', 'LinkUrl': '', 'CollectionGuid': '',
           'Href': '', 'IsComment': False, 'IsCreateHTML': None, 'Page': 0, 'ChannelNo': 'QT',
           'ParentChannelNoGuid': '174087b8-0b4b-4224-af9a-fe1c9fb74f3b', 'ParentChannelNo': 'Collection',
           'ChannelName': '青铜器',
           'FullParentChannel': 'bed44b89-67e5-4ecc-952b-d2ae6a2e01fc|174087b8-0b4b-4224-af9a-fe1c9fb74f3b|c54b5946-8028-4d1a-9d88-64bee7ef9969',
           'IsSyncMedia': True, 'RatingScore': None, 'McrName': '', 'Matter': '', 'comAgeTypeID3': '',
           'comAgeTypeID2': '', 'comAgeTypeID1': '', 'comAgeTypeID': '', 'App3D': '', 'Web3D': '', 'SpecificSize': None,
           'CommentCount': 0, 'AllCommentCount': 0}],
 'PageCount': 20,
 'CurrentPage': 1,
 'Total': 192,
 'PageSize': 10,
 'ReserveSeatNum': '', 'ImagesWaterUrl': 'http://file.hbww.org/WaterMark/',
 'ImagesThumbUrl': 'http://file.hbww.org/Thumb300/', 'ImagesThumb100Url': 'http://file.hbww.org/Thumb100/',
 'ImagesThumbCoverUrl': 'http://file.hbww.org/ThumbCover/'}
