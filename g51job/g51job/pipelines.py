# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient
from scrapy.exporters import JsonItemExporter

#存入数据库
url = 'mongodb://root:chen@127.0.0.1:27017/g51job'
client = MongoClient(url)

collection = client['g51job']["job"]

class G51JobPipeline:
    def open_spider(self,spider):#spider开启事，方法被调用
        self.file = open('./job.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8')
        self.exporter.start_exporting()
        self.count = 0    
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    
    def process_item(self, item, spider):
        #print(item)
        #self.exporter.export_item(item)
        
        self.count += 1
        print(self.count,'-------',item)
        collection.insert(item)
        return item
