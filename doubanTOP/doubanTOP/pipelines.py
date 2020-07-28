# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
import pymysql
from .settings import mysql_host, db_user, db_password, db_name
import pymongo
from .settings import MONGO_URL, MONGO_DB


class DoubantopPipeline(object):
    def __init__(self):
        self.host = mysql_host
        self.user = db_user
        self.dbpwd = db_password
        self.dbname = db_name

        # self.connect = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        self.conn = self.connect = pymysql.connect(host=self.host, user=self.user, password=self.dbpwd, db=self.dbname)
        self.cursor = self.connect.cursor()
        print('连接数据库成功')

        # 定义mongoDB
        self.mongo_url = MONGO_URL
        self.mongo_db = MONGO_DB

        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        print('mongoBD连接成功')

    def process_item(self, item, spider):
        # 保存csv文件
        # 数据库、sql语句、cursor

        # 定义要执行的SQL语句
        sql = 'insert into tops(serial_number,movie_name,describe,start,award,evaluate)VALUES (%s,%s,%s,%s,%s,%s)'
        # 执行SQL语句
        self.cursor.execute(sql, (
        item['serial_number'], item['movie_name'], item['describe'], item['start'], item['award'],
        item['evaluate']))
        self.connect.commit()

        '''
        #存储数据到MongoDB
        data={'serial_number':item['serial_number'],
              'movie_name':item['movie_name'],
              'introduce':item['introduce'],
              'description':item['description'],
              'star':item['star'],
              'evaluate':item['evaluate'],
              }
        '''
        self.table = self.db['top250']
        self.table.insert(dict(item))
        print('数据插入mongoDB成功')
        return item

    def close_spider(self, spider):
        # 关闭光标对象
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()

        #关闭mongoDB
        self.client.close()