# -*- coding: utf-8 -*-
import scrapy
from settings import set_keyword
# from selenium import webdriver


def _baidu_url(keyword, page_count):
    default_url = 'http://www.baidu.com/s?wd={0}'.format(keyword)
    default_page_url = default_url + '&pn=%d0'
    url_list = [default_page_url % i for i in range(1, page_count-1)]
    urls = [default_url]
    urls.extend(url_list)
    return urls


class SearchBaiduSpider(scrapy.Spider):
    name = 'search_baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = []

    def __init__(self, keyword, page_count=2, *args, **kwargs):
        self.keyword = keyword
        set_keyword(keyword)
        print("set_keyword" + keyword)
        super(SearchBaiduSpider, self).__init__(*args, **kwargs)
        self.start_urls = _baidu_url(keyword, int(page_count))

    def parse(self, response):
        for cell in response.xpath('//h3[@class="t"]'):
            text = cell.xpath('.//a[@data-click]').re(r'">(.*)</a>')
            text = text[0]
            text = text.replace("<em>", "").replace("</em>", "")
            url = cell.xpath('.//@href').extract_first()
            from items import ScrapySearchItem
            item = ScrapySearchItem()
            item['keyword'] = self.keyword
            item['text'] = text
            item['url'] = url
            item['origin'] = 'baidu'
            yield item


def _google_url(keywork, page_count):
    default_url = 'http://www.google.com/search?q={0}'.format(keywork)
    default_page_url = default_url + '&start=%d0'
    url_list = [default_page_url % i for i in range(1, page_count - 1)]
    urls = [default_url]
    urls.extend(url_list)
    return urls


class SearchGoogleSpider(scrapy.Spider):
    name = 'search_google'
    allowed_domains = ['www.google.com']
    start_urls = ''
    print(start_urls)

    def __init__(self, keyword, page_count=2, *args, **kwargs):
        self.keyword = keyword
        set_keyword(keyword)
        print("set_keyword" + keyword)
        super(SearchGoogleSpider, self).__init__(*args, **kwargs)
        self.start_urls = _google_url(keyword, int(page_count))

    def parse(self, response):
        for cell in response.xpath('//div[@class="g"]/h3[@class="r"]/a'):
            url = cell.xpath('./@href').extract_first()
            text = cell.re(r'">(.*)</a>')
            text = text[0]
            text = text.replace("<b>", "").replace("</b>", "")
            from items import ScrapySearchItem
            item = ScrapySearchItem()
            item['keyword'] = self.keyword
            item['url'] = 'https://www.google.com' + url
            item['text'] = text
            item['origin'] = 'google'
            yield item
            