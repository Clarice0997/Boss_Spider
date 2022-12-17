import scrapy
from scrapy import Request
from boss.items import BossItem


class JobspiderSpider(scrapy.Spider):
    name = 'jobspider'
    allowed_domains = ['www.zhipin.com']

    def __init__(self, kwd):
        self.kwd=kwd
        self.start_urls =f'https://www.zhipin.com/web/geek/job?query={kwd}&city=100010000'

    def start_requests(self):
        yield Request(self.start_urls,meta={'flag':"false"},callback=self.parse)

    def parse(self, response):
        job_list=response.css("li.job-card-wrapper")
        next_page=response.css("div.options-pages>a:last-child::attr(class)").extract_first()
        page=int(response.css("div.options-pages>a.selected::text").extract_first())+1
        print("type---"+str(type(page)))
        print(job_list)
        for i in job_list:
            job_name=i.css("span.job-name::text").extract_first()
            city_name =i.css("span.job-area::text").extract_first()
            if city_name.find("·")>-1:
                city_name=city_name.split("·")[0]
            brand_name=i.css("h3.company-name>a::text").extract_first()
            salaryDesc=i.css("span.salary::text").extract_first()
            jobExperience=i.css("ul.tag-list>li:nth-child(1)::text").extract_first()
            jobDegree=i.css("ul.tag-list>li:nth-child(2)::text").extract_first()
            item = BossItem()
            item['jobkwd']=self.kwd
            item['jobName']=job_name
            item['cityName']=city_name
            item['companyName']=brand_name
            item['salaryDesc']=salaryDesc
            item['jobExperience']=jobExperience
            item['jobDegree']=jobDegree
            print(item)
            yield item
        if not next_page and page<=5:
            next_url = self.start_urls + "&page=" + str(page)

            yield scrapy.Request(url=next_url,meta={'flag':"true"}, callback=self.parse,dont_filter=True)

    def close(spider, reason):
        print("爬虫运行完毕")




