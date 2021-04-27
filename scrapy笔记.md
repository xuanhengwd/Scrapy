# scrapy笔记

## 远程部署

**见部署文档**

## 安装框架

pip install scrapy

windows下  要安装 pip install pypiwin32

## 创建项目和爬虫

1. 创建项目：`scrapy startproject xxx`
2. 创建爬虫：进入项目的路径，执行： `scrapy genspider  爬虫名字 爬虫域名`

注意：爬虫名不能和项目名一样。

## 目录结构

1. items.py：可以保存爬取到的数据，相当于存储爬取到的数据的容器。
2. middlewares.py：爬虫项目的中间件文件.
3. pipelines.py：爬虫项目的管道文件，用来对items中的数据进行进一步的加工处理。用来将items的模型存储到本地磁盘中
4.  settings.py：爬虫项目的设置文件，包含了爬虫项目的配置信息。（比如请求头，多久发送一次，ip代理池等）
5.  scrapy.cfg：爬虫项目的配置文件。
6. spider包：以后所有的爬虫，都是存放在这里面

## 一些设置

```python
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```

改成false 以防没有robots.txt



```python
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}
```

添加最后一行'User-Agent': 更换一个代理，这样进行伪装（可以用百度，在开发者工具里面）。

## 运行

`scrapy crawl 爬虫名`

根目录创建一个py文件，可以直接运行

```python
from scrapy import cmdline
#列表“”里面是命令行
cmdline.execute("scrapy crawl test".split())
```

## 4.11保存（json）

导包试遇到了问题

```python
from scrapystudy.scrapystudy.items import ScrapystudyItem
```

```shell
#报错
from scrapystudy.scrapystudy.items import ScrapystudyItem
ModuleNotFoundError: No module named 'scrapystudy.scrapystudy'
```

正确做法

```
from ..items import ScrapystudyItem
```

虽然我也不知道上面那样为啥不行。

### 一些方法

1. response是一个`scrapy.http.response.html.HtmlResponse`对象，可以执行`xpath`和`css`语法来提取数据。
2. 提取出来的数据，是一个`Selector`或者是一个`SelectorList`对象。如果想要获取其中的字符串，那么应该执行`getall`或者`get`方法。
3. getall方法：获取`Selector`中的所以文本，返回的是一个列表。
4. get方法：获取的是`Selector`中的第一个文本。返回的是一个str。
5. 如果数据解析回来，要传给pipline处理。那么可以使用`yield`来返回。或者收集所以item，最后统一return。
6. item：建议在`items.py`中定义好模型，以后就不用使用字典。
7. pipeline：专门保存数据，三个方法
   - `def open_spider(self, spider):`当爬虫打开时执行
   - `def process_item(self, item, spider):`当爬虫有item传来时调用
   - `def close_spider(self, spider):`关闭时调用

激活pipeline：settings.py中，打开如下

```python
ITEM_PIPELINES = {
   'scrapystudy.pipelines.ScrapystudyPipeline': 300,
}
```

### 两个类

**JsonItemExporter和JsonLinesItemExporter**

保存json数据使用这两个类更加的简单

1. `JsonItemExporter`：是每次把数据添加到内存中，最后统一写入磁盘。好处：存储的是一个满足json规则的数据。坏处：数据量大，比较消耗内存

   示例代码：

   ```python
   class ScrapystudyPipeline:
       def __init__(self):
           self.fp = open("duanzi.json", 'wb')
           self.exporter = JsonItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
           self.exporter.start_exporting()
   
       def open_spider(self, spider):
           print("start....")
   
       def process_item(self, item, spider):
           # 可以保存中文ensure_ascii=False,dict转成字典
           # item_json = json.dumps(dict(item), ensure_ascii=False)
           # self.fp.write(item_json + '\n')
           self.exporter.export_item(item)
           return item
   
       def close_spider(self, spider):
           self.exporter.finish_exporting()
           self.fp.close()
           print("over....")
   ```

2. `JsonLinesItemExporter`：这个是每次调用`export_item`的时候就把这个item存储到硬盘中。坏处：每个字典是一行，整个文件不满足json格式。好处：不会耗内存，数据比较安全

   示例代码：

   ```python
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
   ```


## CrawSpider

需要使用`LinkExtractor`和`Rule`，这两个东西决定爬虫的具体走向。

执行： `scrapy genspider -t crawl 爬虫名字 爬虫域名`

1. allow设置规则的方法：要能够限制在我们想要的url上面。不要跟其他的url产生相同的正则表达式即可。
2. 什么情况下使用follow：如果在爬取页面的时候，需要将满足当前条件的url在进行跟进，那么设置为True，否则为False
3. 什么情况下该指定callback：如果这个url对应的页面，只是为了获取更多的url，并不需要里面的数据，那么可以不指定callback。如果想要获取url对应页面的数据，那么就需要指定一个callback。

实例代码：

```python
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ScrapystudyItem


class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['www.wxapp-union.com']
    start_urls = ['https://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r".+article-.+\.html"), callback="parse_detail", follow=False)
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='ph']/text()").get()
        author_p = response.xpath("//p[@class='authors']")
        author = author_p.xpath(".//a/text()").get()
        pub_time = author_p.xpath(".//span/text()").get()
        article_content = response.xpath("//td[@id='article_content']//text()").getall()
        content = "".join(article_content).strip()
        item = ScrapystudyItem(title=title, author=author, pub_time=pub_time, content=content)
        yield item
```

## 爬取存入mysql

### 两个方法

两者方法 见示例

**第一种**

```python
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
```

**第二种**

```python
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
```

### 更新方法

**第一种**

sql语句中加入`on duplicate key update`后面是要修改的值

```python
self._sql = """
insert into text1(id,num,name) values (%s,%s,%s)
 on duplicate key update num =values (num),name =values (name )
"""
```

**第二种**

用`replace into`

 1）如果主键值重复，那么覆盖表中已有的行       

 2）如果没有主键值重复，则插入该行

```python
self._sql = """
            replace into text1(id,num,name) values (%s,%s,%s)
            """
```

## 爬取网页 网页显示的结构和真实结构不一样

见`NjMuseum.py` 

```python
#网上级标签寻找，找到有输出的，然后查看输出文字的标签
#或者分析网页的结构 判断是第几个标签 用数字代替class
col_info=response.xpath("//div[@class='basicrightcon']/div[3]").get()
```