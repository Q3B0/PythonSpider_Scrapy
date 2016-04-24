#-*-encoding:utf-8-*-
from scrapy.spiders import CrawlSpider
from scrapy import Request
from scrapy import Selector
from TSRCW.items import TsrcwItem
from bs4 import BeautifulSoup
import random
import re

class TsrcwSpider(CrawlSpider):
    name = 'tsrcwSpider'
    start_urls = ['http://www.tsrcw.com/']
    header = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    baseUrl = 'http://www.tsrcw.com/'
    mailre = re.compile(r'([a-zA-Z0-9]+@[a-zA-Z0-9]+\.?[a-zA-Z0-9]+\.+[a-zA-Z0-9]+)')
    def start_requests(self):
        yield Request(self.start_urls[0], headers=random.choice(self.header))

    def parse(self, response):
        selector = Selector(response)
        table = selector.xpath('//table[@id="DataList7"]//td[@class="ad_boder"]/a/@href')
        table2 = selector.xpath('//table[@id="DataList9"]//td[@class="career"]/a/@href')
        for url in table:
            target_url = self.baseUrl + url.extract()
            yield Request(target_url, headers=random.choice(self.header), callback=self.parse_item)
        for url in table2:
            target_url = self.baseUrl + url.extract()
            yield Request(target_url, headers=random.choice(self.header), callback=self.parse_item)

    def parse_item(self, response):

        selector = Selector(response)
        companyInfo = selector.xpath('//td[@class="cont_company"]//td[@class="td_r"]/text()')
        jobInfo = selector.xpath('//*[@id="DataList1"]//table/tr')
        contactInfo = selector.xpath('//td[@class="cont_contact"]')
        contact_text = contactInfo.xpath('text()').extract()[0] + ' ' + contactInfo.xpath('text()').extract()[1] + ' ' + contactInfo.xpath('text()').extract()[2]

        #print self.mailre.findall(contact_text)
        #print self.phonePartern.match(contactInfo.xpath('text()').extract()[0])
        #print self.emainPartern(contactInfo.xpath('text()').extract()[1])
        #print (contactInfo.xpath('text()').extract()[2]).replace(' ','')

        for each in jobInfo:
            item = TsrcwItem()
            print each.extract()
            jobList = []
            try:
                for i in each.xpath('td[@class="td-grey"]/text()'):
                    if not (i.extract()).strip() == "":
                        jobList.append((i.extract()).strip())
                item['email'] = self.mailre.findall(contact_text)[0]
                item['companyName'] = (companyInfo.extract()[0]).strip()
                item['industryName'] = (companyInfo.extract()[1]).strip()
                item['companyNature'] = (companyInfo.extract()[2]).strip()
                item['jobName'] = (each.xpath('td[@class="td-grey"]/a/text()').extract()[0]).strip()
                item['jobDetail'] = self.baseUrl+(each.xpath('td[@class="td-grey"]/a/@href').extract()[0]).strip()
                item['jobRegion'] = jobList[0]
                item['requiredDegree'] = jobList[1]
                item['salary'] = jobList[2]
                item['endDate'] = jobList[3]
                yield item
            except Exception,e:
                continue

