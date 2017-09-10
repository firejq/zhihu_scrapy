# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from zhihu_scrapy import settings


class MongoPipeline(object):
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(settings.MONGO_URI)
        # 数据库登录帐号密码
        # self.client.admin.authenticate(settings['MINGO_USER'],
        # settings['MONGO_PSW'])
        # 获得数据库句柄
        self.db = self.client[settings.MONGO_DB]
        # 获得collection句柄
        self.collection = self.db[settings.MONGO_COLLECTION]

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.collection.update(
                {'url_token': item['url_token']}, {'$set': dict(item)}, True
            )
        except BaseException as error:
            print("出现错误: " + error.__str__())
        return item
