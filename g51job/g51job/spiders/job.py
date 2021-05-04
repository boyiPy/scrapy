import scrapy
import re
import json

class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/110300,000000,0000,00,9,99,%2B,2,1.html']
    url = 'https://search.51job.com/list/110300,000000,0000,00,9,99,+,2,%d.html'
    page_num = 2
    def parse(self, response):
        #print(response.text)
        """
        数据放入html中js模块，而不是网页所显示的标签
        div_list = response.xpath('//div[@class="j_joblist"]')
        print(div_list)
        for div in div_list:
            item = {}
            item["job"] = div.xpath('./a/p[1]/span[1]/@title/text()').extract_first()
            item['publish_date'] = div.xpath('.//span[@class="time"]/text()').extract_first()
            item['company'] = div.xpath('.//a[@class="cname"]/text()').extract_first()
            yield
        """

        p = re.compile('window.__SEARCH_RESULT__ =.*?script>')
        text = re.findall(p,response.text)[0]
        print('response.text---------->',text,'\r\n-------------')
        d_list = re.findall('{"type".*?:""}',text)
        #print(d_list)
        for d in d_list:
            item = {}
            #print('---------',d)
            #print(type(d))
            c = json.loads(d)
            #print(type(c))
            #print(c['job_name'])
            item['job_name'] = c['job_name']
            item['company_name'] = c['company_name']
            item['workarea_text'] = c['workarea_text']
            item['providesalary'] = c['providesalary_text']
            #print(item)
            yield item
        #取不到结果,可能是防盗链的原因，经过测试是allowed_domains写错将我url过滤掉了
        
        if self.page_num < 10:
            next_url = format(self.url%self.page_num)
            print(next_url)
            self.page_num += 1
            yield scrapy.Request(next_url,callback=self.parse)
        
