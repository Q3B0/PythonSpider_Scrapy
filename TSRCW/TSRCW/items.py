# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class TsrcwItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    companyName = Field()   #公司名称
    industryName = Field()  #行业
    companyNature = Field() #企业性质
    jobName = Field()       #工作名称
    jobRegion = Field()     #工作地区
    requiredDegree = Field()#学历要求
    salary = Field()        #薪资
    endDate = Field()       #截止日期
    jobDetail = Field()     #详情地址
    contact = Field()       #联系人
    tel = Field()           #联系电话
    fax = Field()           #联系传真
    email = Field()         #电邮
