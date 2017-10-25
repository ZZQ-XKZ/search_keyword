# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from msic.common import utils
import hashlib
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declared_attr
from settings import get_keyword


class ScrapySearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    keyword = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
    origin = scrapy.Field()
    pass


Base = declarative_base()


class ScrapySQLItem(Base):
    @declared_attr
    def __tablename__(cls):
        return get_keyword()
    md5 = Column(String(32), primary_key=True)
    create_time = Column(DateTime)
    url = Column(String(512))
    origin = Column(String(32))
    text = Column(String(256))
    
    @staticmethod
    def create(scrapy_itme):
        item = ScrapySQLItem()
        item.text = scrapy_itme['text'].encode('utf-8')
        m = hashlib.md5()
        m.update(item.text)
        item.md5 = m.hexdigest()
        item.url = scrapy_itme['url'].encode('utf-8')
        item.origin = scrapy_itme['origin']
        item.create_time = utils.get_utc_date() 
        return item
        
    @staticmethod
    def create_table(engine):
        Base.metadata.create_all(engine)

        
