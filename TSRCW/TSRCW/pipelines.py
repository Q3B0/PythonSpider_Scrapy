# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import TsrcwItem
from scrapy.conf import settings
import pymongo

class TsrcwPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        try:
            client = pymongo.MongoClient(host=host, port=port)
            tdb = client[dbName]
            self.post = tdb[settings['MONGODB_DOCNAME']]
        except Exception, e:
            print 'error'
    def process_item(self, item, spider):
        jobInfo = dict(item)
        self.post.insert(jobInfo)
        return item
