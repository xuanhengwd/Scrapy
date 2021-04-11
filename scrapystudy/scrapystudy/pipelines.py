# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

# class ScrapystudyPipeline:
#     def __init__(self):
#         self.fp = open("duanzi.json", 'w', encoding='utf-8')
#
#     def open_spider(self, spider):
#         print("start....")
#
#     def process_item(self, item, spider):
#         # 可以保存中文ensure_ascii=False,dict转成字典
#         item_json = json.dumps(dict(item), ensure_ascii=False)
#         self.fp.write(item_json + '\n')
#         return item
#
#     def close_spider(self, spider):
#         self.fp.close()
#         print("over....")

from scrapy.exporters import JsonItemExporter


# class ScrapystudyPipeline:
#     def __init__(self):
#         self.fp = open("duanzi.json", 'wb')
#         self.exporter = JsonItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
#         self.exporter.start_exporting()
#
#     def open_spider(self, spider):
#         print("start....")
#
#     def process_item(self, item, spider):
#         # 可以保存中文ensure_ascii=False,dict转成字典
#         # item_json = json.dumps(dict(item), ensure_ascii=False)
#         # self.fp.write(item_json + '\n')
#         self.exporter.export_item(item)
#         return item
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.fp.close()
#         print("over....")

from scrapy.exporters import JsonLinesItemExporter

class ScrapystudyPipeline:
    def __init__(self):
        self.fp = open("duanzi.json", 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        self.exporter.start_exporting()

    def open_spider(self, spider):
        print("start....")

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()
        print("over....")

