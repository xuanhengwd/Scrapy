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




# class ScrapystudyPipeline:
#     def __init__(self):
#
#         #self.fp = open("handan.json", 'wb')
#
#         #self.fp = open("object.json", 'wb')
#         #self.fp = open("duanzi.json", 'wb')
#         #self.fp=open("wxjc.json",'wb')
#         self.fp = open("hhh.json", 'wb')
#         self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
#         self.exporter.start_exporting()
#
#
#     def open_spider(self, spider):
#         print("start....")
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def close_spider(self, spider):
#         self.fp.close()
#         print("over....")
#

class HandanPipleline:
    def __init__(self):
        self.fp = open("handan.json", 'wb')
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


class DuanziPipleline:
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
import pymysql
class ScrapystudyPipeline:
    def __init__(self):
        #各种参数
        dbparams={
            'host':'123.56.13.242',
            'port':3306,
            'user':'root',
            'password':'Aliyun2021',
            'database':'test',
            'charset':'utf8'
        }
        #连接
        self.conn=pymysql.connect(**dbparams)
        #调用cursor方法
        self.cursor=self.conn.cursor()
        self._sql=None
    def process_item(self, item, spider):
        #运行
        self.cursor.execute(self.sql,(item['id'],item['name'],item['introduction']))
        #存入数据库
        self.conn.commit()
        return item

    #属性
    @property
    def sql(self):
        if not self._sql:
            self._sql="""
            insert into collection(id,name,introduction) values (%s,%s,%s)
            """
            return self._sql
        return self._sql


#优化的
from twisted.enterprise import adbapi
from pymysql import cursors
class ScrapystudygogoPipeline:
    def __init__(self):
        #参数
        dbparams={
            'host':'123.56.13.242',
            'port':3306,
            'user':'root',
            'password':'Aliyun2021',
            'database':'test',
            'charset':'utf8',
            'cursorclass':cursors.DictCursor
        }
        #用ConnectionPool连接池，效率提高
        self.dbpool=adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql=None

    @property
    def sql(self):
        if not self._sql:
            self._sql="""
            insert into collection(id,name,introduction) values (%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer=self.dbpool.runInteraction(self.insert_item,item)
        #错误信息
        defer.addErrback(self.handle_error,item,spider)
    def insert_item(self,cursor,item):
        #插入
        cursor.execute(self.sql,(item['id'],item['name'],item['introduction']))

    def handle_error(self,error,item,spider):
        print("="*10+"error"+"="*10)
        print(error)
        print("=" * 10 + "error" + "=" * 10)


class QhmuseumPipeline:
    def __init__(self):
        #参数
        dbparams={
            'host':'123.56.13.242',
            'port':3306,
            'user':'root',
            'password':'Aliyun2021',
            'database':'museum',
            'charset':'utf8',
            'cursorclass':cursors.DictCursor
        }
        #用ConnectionPool连接池，效率提高
        self.dbpool=adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql=None

    @property
    def sql(self):
        if not self._sql:
            self._sql="""
            insert into Collection(col_id,mus_id,col_name,col_era,
            col_info,mus_name,col_picture) values (%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer=self.dbpool.runInteraction(self.insert_item,item)
        #错误信息
        defer.addErrback(self.handle_error,item,spider)
    def insert_item(self,cursor,item):
        #插入
        cursor.execute(self.sql,(item['col_id'],item['mus_id'],item['col_name'],item['col_era'],
                                 item['col_info'],item['mus_name'],item['col_picture']))

    def handle_error(self,error,item,spider):
        print("="*10+"error"+"="*10)
        print(error)
        print("=" * 10 + "error" + "=" * 10)

class QhmuseumexPipeline:
    def __init__(self):
        # 各种参数
        dbparams = {
            'host': '123.56.13.242',
            'port': 3306,
            'user': 'root',
            'password': 'Aliyun2021',
            'database': 'museum',
            'charset': 'utf8'
        }
        # 连接
        self.conn = pymysql.connect(**dbparams)
        # 调用cursor方法
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        # 运行
        self.cursor.execute(self.sql, (item["exh_id"],item["exh_name"],item["mus_id"],item["mus_name"],item["exh_info"],item["exh_picture"],item["exh_time"]))
        # 存入数据库
        self.conn.commit()
        return item

        # 属性

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
               insert into Exhibition(exh_id,exh_name,mus_id,mus_name,exh_info,exh_picture,exh_time) values (%s,%s,%s,%s,%s,%s,%s)
               """
            return self._sql
        return self._sql


class TextPipeline:
    def __init__(self):
        # 参数
        dbparams = {
            'host': '123.56.13.242',
            'port': 3306,
            'user': 'root',
            'password': 'Aliyun2021',
            'database': 'test',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        # 用ConnectionPool连接池，效率提高
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            # self._sql = """
            # insert into text1(id,num,name) values (%s,%s,%s)
            #  on duplicate key update num =values (num),name =values (name )
            # """
            self._sql = """
                        replace into text1(id,num,name) values (%s,%s,%s)
                        """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        # 错误信息
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        # 插入
        cursor.execute(self.sql, (item['id'], item['num'],item['name']))

    def handle_error(self, error, item, spider):
        print("=" * 10 + "error" + "=" * 10)
        print(error)
        print("=" * 10 + "error" + "=" * 10)

class NjmuseumPipeline:
    def __init__(self):
        # 各种参数
        dbparams = {
            'host': '123.56.13.242',
            'port': 3306,
            'user': 'root',
            'password': 'Aliyun2021',
            'database': 'museum',
            'charset': 'utf8'
        }
        # 连接
        self.conn = pymysql.connect(**dbparams)
        # 调用cursor方法
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        # 运行
        self.cursor.execute(self.sql, (item['col_id'],item['mus_id'],item['col_name'],item['col_era'],
                                 item['col_info'],item['mus_name'],item['col_picture']))
        # 存入数据库
        self.conn.commit()
        return item

    # 属性
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            replace into Collection(col_id,mus_id,col_name,col_era,
            col_info,mus_name,col_picture) values (%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

class MuseumPipeline:
    def __init__(self):
        #参数
        dbparams={
            'host':'123.56.13.242',
            'port':3306,
            'user':'root',
            'password':'Aliyun2021',
            'database':'museum',
            'charset':'utf8',
            'cursorclass':cursors.DictCursor
        }
        #用ConnectionPool连接池，效率提高
        self.dbpool=adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql=None

    @property
    def sql(self):
        if not self._sql:
            self._sql="""
            replace into Collection(col_id,mus_id,col_name,col_era,
            col_info,mus_name,col_picture) values (%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer=self.dbpool.runInteraction(self.insert_item,item)
        #错误信息
        defer.addErrback(self.handle_error,item,spider)
    def insert_item(self,cursor,item):
        #插入
        cursor.execute(self.sql,(item['col_id'],item['mus_id'],item['col_name'],item['col_era'],
                                 item['col_info'],item['mus_name'],item['col_picture']))

    def handle_error(self,error,item,spider):
        print("="*10+"error"+"="*10)
        print(error)
        print("=" * 10 + "error" + "=" * 10)

class MuseumExPipeline:
    def __init__(self):
        # 各种参数
        dbparams = {
            'host': '123.56.13.242',
            'port': 3306,
            'user': 'root',
            'password': 'Aliyun2021',
            'database': 'museum',
            'charset': 'utf8'
        }
        # 连接
        self.conn = pymysql.connect(**dbparams)
        # 调用cursor方法
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        # 运行
        self.cursor.execute(self.sql, (item["exh_id"],item["exh_name"],item["mus_id"],item["mus_name"],item["exh_info"],item["exh_picture"],item["exh_time"]))
        # 存入数据库
        self.conn.commit()
        return item

        # 属性

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
               replace into Exhibition(exh_id,exh_name,mus_id,mus_name,exh_info,exh_picture,exh_time) values (%s,%s,%s,%s,%s,%s,%s)
               """
            return self._sql
        return self._sql