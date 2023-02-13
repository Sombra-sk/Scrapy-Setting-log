import scrapy
import re
from lxml import etree
from xml.etree import ElementTree
import json
from bs4 import BeautifulSoup
import os

from chengxu.settings import DATA_PATH
from chengxu.settings import headers

cookie = {
    'cookie': 'JSESSIONID=86cd0804-e1d6-4fb4-9d09-2ea849febe1a; TXGAID=86cd0804-e1d6-4fb4-9d09-2ea849febe1a; oneapmclientid=181f645554d15b-0e3f7a370d17e1-26021851-15f900-181f645554ea15; _gcl_au=1.1.1902652408.1657694159; AGL_USER_ID=b1cf0606-60df-42bb-8cab-f172a62d5f89; Hm_lvt_ffd8a15e592c62913e779f8d375afb9a=1657694161; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross={"distinct_id":"181f6459a86de2-00867526a74d57-26021851-1440000-181f6459a87e15","first_id":"","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":""},"$device_id":"181f6459a86de2-00867526a74d57-26021851-1440000-181f6459a87e15"}; oneapmbiswitch=event=0; ONEAPM_BI_sessionid=9134.914|1657697780082|; Hm_lpvt_ffd8a15e592c62913e779f8d375afb9a=1657699171; xbluewareid=1E5rzuBTWQshiA0WgTcl'
}


class TxgaSpider(scrapy.Spider):
    name = 'txga'
    start_urls = ['https://www.txga.com/productcenter.html']

    def parse(self, response):
        tree = etree.HTML(response.text)
        a_list = tree.xpath('//*[@id="productcenter"]/div/ul/li/div[2]/a')
        for a in a_list:
            title_1 = a.xpath('./text()')[0]
            title_1 = title_1.strip()
            href = a.xpath('./@href')[0]
            href = 'https://www.txga.com' + href
            yield scrapy.Request(href, headers=headers, callback=self.parse_url,
                                 meta={'title_1': title_1})

    def parse_url(self, response):
        title_1 = response.meta['title_1']
        url = response.url
        tree = response.text
        source = etree.HTML(response.text)
        group2 = re.findall(r"var group2 = '(.*?)'", tree)[0]
        group3 = re.findall(r"var group3 = '(.*?)'", tree)[0]
        page_list = re.findall(r'goodsNum="(\d+)"', tree)[0]
        page_list = int(int(page_list) / 24 + 1)
        for page in range(1, page_list + 1):
            link = 'https://www.txga.com/searchSerialByOpts?group1=&group2=' + group2 + '&group3=&group4=&group5=&group6=&group7=&current=&voltage=&page=' + str(
                page) + '&limit=24&keywords=&onlyHasStock=N&t=1657701775502'
            yield scrapy.Request(link, headers=headers, callback=self.parse_json,
                                 meta={'title_1': title_1, 'url': url, 'page': page})

    def parse_json(self, response):
        page = response.meta['page']
        url = response.meta['url']
        title_1 = response.meta['title_1']
        title_1 = re.sub(r'[\\/:*?"<>|]', '-', title_1)
        link = response.url
        scurce = json.loads(response.text)
        data_list = scurce['data']['list']
        for data in data_list:
            # print(data)
            code = re.findall(r"'code': '(.*?)'", str(data))[0]
            # print(code)
            href = 'https://www.txga.com/serialOnSaleProducts?serialCode=' + code
            # print(url)
            yield scrapy.Request(href, headers=headers, callback=self.parse_json_t,
                                 meta={'title_1': title_1, 'url': url, 'page': page, 'code': code})

    def parse_json_t(self, response):
        code = response.meta['code']
        page = response.meta['page']
        url = response.meta['url']
        title_1 = response.meta['title_1']
        title_1 = re.sub(r'[\\/:*?"<>|]', '-', title_1)
        link = response.url
        scurce = json.loads(response.text)
        data_list = scurce['data']
        for data in data_list:
            # print(data)
            code_p = re.findall(r"'code': '(.*?)'", str(data))[0]
            # print(code)
            href = 'https://www.txga.com/product-details/' + code_p + '.html'
            # print(href)
            yield scrapy.Request(href, headers=headers, callback=self.parse_html, meta={'code': code_p})

    def parse_html(self, response):
        code = response.meta['code']
        path = rf'{DATA_PATH}/txga V1.1/HTML'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(rf'{path}/{code}.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
