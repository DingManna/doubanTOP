from scrapy import cmdline
from logger import LOG

cmdline.execute('scrapy crawl douban_spider -o douban_data.csv'.split())
# 控制台输出  加上写入csv文件
# 这个douban_data.csv就是输出的那个csv文件名

LOG.info('finish')
