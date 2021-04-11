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

3. 

