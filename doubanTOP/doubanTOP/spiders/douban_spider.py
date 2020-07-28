import scrapy

# from ..items import DoubantopItem
from ..items import DoubantopItem
import re
import requests
from bs4 import BeautifulSoup
import json
import xlwt

headers = {
        'user-agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"',
        'Host': 'movie.douban.com'
    }

allitems = []


class DemoSpider(scrapy.Spider):
    # 爬虫的名称
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 起始的 URL
    start_urls = ["https://movie.douban.com/top250"]

    # scrapy 默认的解析方法， response：解析结果
    def parse(self, response):
        count = 1
        # 解析第一页的数据
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")

        # allitems = []

        for i_item in movie_list:

            # 实例化 Item 对象
            douban_item = DoubantopItem()
            urlThis = []

            # 设置并获取详细的数据
            serial_number = douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            movie_name = douban_item['movie_name'] = i_item.xpath(
                ".//div[@class='info']//div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']//p[1]/text()").extract()

            # 二进制下载图片
            cover = i_item.xpath(".//div[@class='item']/div[@class='pic']/a/img/@src").extract()
            cover_name = douban_item['movie_name']
            # 电影图片下载
            print("123")
            for url in cover:
                print("111")
                path = '/Users/tanyou/Desktop/doubanTOP/doubanTOP/doubanTOP/douban/'
                pic = requests.get(url=url, timeout=15)
                string = str(cover_name) + '.jpg'
                with open(path + string, 'wb') as f:
                    f.write(pic.content)
                    print('成功下载图片: %s' % (str(cover_name)))

            # 遇到多行数 据需要进行字符串的处理
            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['instruce'] = content_s
            start = douban_item['start'] = i_item.xpath(".//div[@class='info']//div[@class='bd']//span["
                                                "@class='rating_num']/text()").extract_first()

            evaluate = douban_item['evaluate'] = i_item.xpath(".//div[@class='item']//div[@class='info']//div["
                                                   "@class='bd']//span[4]/text()").extract_first()

            describe = douban_item['describe'] = i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//p["
                                                       "@class='quote']/span[1]/text()").extract_first()
            # douban_item['childURL'] = i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='hd']//a/@href").extract_first()
            urlThis = i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='hd']//a/@href").extract_first()
            #解析详情页面
            #res = requests.get(douban_item['childURL'], headers=headers)
            res = requests.get(urlThis, headers=headers)
            soup = BeautifulSoup(res.text, 'lxml')
            awards = soup.find_all('ul', {'class': 'award'})
            awardList = []
            for each in awards:
                award = each.text.replace("\n", "")
                award = award.replace("/", "")
                #处理一下\xa0\xa0这种特殊符号
                award = "".join(award.split())
                # print(award)
                awardList.append(award)
            award = douban_item['award'] = awardList

            allitem = {'award': award,
                       'describe': describe,
                       'evaluate': evaluate,
                       'movie_name': movie_name,
                       'serial_number': serial_number,
                       'start': start}
            allitems.append(allitem)


            # 将数据给 pipelines
            yield douban_item

        # 存入json文件
        with open('../doubanTOP/doubantop250.json', 'a', encoding='utf-8')as fp:
            #with open('/Users/tanyou/Desktop/doubanTOP/doubanTOP/doubanTOP/doubantop250.json', 'a', encoding='utf-8')as fp:
            fp.write(json.dumps(allitems, ensure_ascii=False))
        print("json文件输入完毕")

        # 存入excel文件
        excelpath = '../doubanTOP/doubantop250.xlsx'
        work_book = xlwt.Workbook(encoding='utf-8')
        sheet = work_book.add_sheet('shuju')
        j = 1  # 从第二行开始
        for ziitem in allitems:
            sheet.write(j, 0, ziitem['award'])  # 第二行,第一列
            sheet.write(j, 1, ziitem['describe'])  # 第二行,第二列
            sheet.write(j, 2, ziitem['evaluate'])
            sheet.write(j, 3, ziitem['movie_name'])
            sheet.write(j, 4, ziitem['serial_number'])
            sheet.write(j, 5, ziitem['start'])
            j += 1
        # 5,保存文件
        work_book.save(excelpath)
        print("excel写入一页成功")

        # 添加剩余条目规则, 使用 xpath 添加 next 链接
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)

