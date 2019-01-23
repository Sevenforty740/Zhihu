# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from settings import *

class MysqlPipline(object):
    def __init__(self):
        self.db = pymysql.connect(
            host = MYSQL_HOST,
            user = MYSQL_USER,
            password = MYSQL_PWD,
            database = MYSQL_DB,
            charset= "utf8"
        )
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        ins = 'insert into zhihu values(%s,%s,%s,%s,%s,%s,%s,%s)'
        L = [item['name'],item['url'],int(item['gender']),item['follower_count'],item['articles_count'],item['answer_count'],item['headline'],item['is_vip']]
        self.cursor.execute(ins,L)
        self.db.commit()

        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()
        print('MySQL数据库断开链接')