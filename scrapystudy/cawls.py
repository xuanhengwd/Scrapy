from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# myspd1是爬虫名
# process.crawl('test')
# process.crawl('handan')

#process.crawl('NjMuseum')
#process.crawl('NjMuseumex')
#process.crawl('XAMuseum')
#process.crawl('XAMuseumex')
# process.crawl('SHtmuseumex')
# process.crawl('JLMuseum')
#process.crawl('JLMuseumex')
# process.crawl('GDMuseum')
#process.crawl('GDMuseumex')
#process.crawl('ZGYDmuseum')
#process.crawl('ZGYDmuseumex')
#process.crawl('NBMuseum')
# process.crawl('NBMuseumex')
# process.crawl('FJMuseum')
# process.crawl('FJMuseumex')
# process.crawl('AYMuseum')
# process.crawl('AYMuseumex')
# process.crawl('HBMuseum')
# process.crawl('HBMuseumex')
# process.crawl('CSJDMuseum')
# process.crawl('CSJDMuseumex')
#process.crawl('GDMJMuseum')
#process.crawl('GDMJMuseumex')
# process.crawl('SXLSMuseum')
# process.crawl('SXLSMuseumex')
# process.crawl('XZMuseum')
# process.crawl('XZMuseumex')
# process.crawl('SXDMuseum')
# process.crawl('SXDMuseumex')
# process.crawl('CHNMuseum')
# process.crawl('DHMuseum')
#process.crawl('DHMuseumex')
# process.crawl('ZGkLMuseum')
# process.crawl('ZGkLMuseumex')
# process.crawl('ZGDYMuseum')
# process.crawl('ZGDYMuseumex')
# process.crawl('LFMuseum')
# process.crawl('LFMuseumex')
# process.crawl('XuZMuseum')
process.crawl('XuZMuseumex')




process.start()