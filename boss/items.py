# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobkwd=scrapy.Field()
    jobName=scrapy.Field() #岗位名称
    cityName=scrapy.Field()#工作区域
    companyName=scrapy.Field()#招聘单位
    salaryDesc=scrapy.Field()#薪酬
    jobExperience=scrapy.Field()#工作经验年限
    jobDegree=scrapy.Field()  #学历

