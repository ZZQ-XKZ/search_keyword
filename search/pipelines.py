# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from msic import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from msic.common.send_email import send_email
import logging


class ScrapySearchItemPipeline(object):
    bInit = False
    def _init(self, spider):
        from items import ScrapySQLItem
        self.engine = create_engine(
            'mysql+mysqldb://'
            + config.MYSQL_USR + ':'
            + config.MYSQL_PASSWD + '@'
            + config.MYSQL_HOST + '/'
            + config.DATABASE_NAME,
            echo=False)
        ScrapySQLItem.create_table(self.engine)
        session_cls = sessionmaker(bind=self.engine)
        self.session = session_cls()
        
    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        if self.bInit is False:
            self._init(spider)
            self.bInit = True
        from items import ScrapySQLItem
        sql_item = ScrapySQLItem.create(item)
        if self.session.query(ScrapySQLItem).filter(ScrapySQLItem.md5 == sql_item.md5).count() <= 0:
            logging.log(logging.INFO, "keyword:" + item['keyword'] + "New item:" + item['text'])
            send_email([item['keyword']], item['text'], item['url'])
            self.session.add(sql_item)
