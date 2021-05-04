import scrapy
import urllib
import re

class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?ie=utf-8&kw=%E7%BE%8E%E5%A5%B3&fr=search']

    def parse(self, response):
        #print('status_code----------->',response.status)
    
        #with open('./t.html','w') as f:
        #    f.write(response.text)
        #正则看似没有问题，但是就是没有结果，是没有加re.S,
        pattern =re.compile(r'li class=" j_thread_list clearfix.*?<a rel="noreferrer" href="(?P<href>.*?)" title="(?P<title>.*?)".*?<.li>',re.S)
        #pattern = "j_threadlist_bright"
        #pattern = re.compile(r'j_thread_list clearfix.*<.li',re.S)
        result_lst = pattern.findall(response.text)
        #print('result->',result_lst)
        for result in result_lst:
                item = {}
                item['href'] = result[0]
                item['title'] = result[1]
                #item['href'] = li.xpath('.//a/@href').extract_first()
                #item['title'] = li.xpath('.//a/@title').extract_first()
                item['img_list'] = []
                if item['href'] is not None:
                    item['href'] = urllib.parse.urljoin(response.url,item['href'])
                    #print(item)
                    yield scrapy.Request(
                        item['href'],
                        callback=self.parse_detail,
                        meta={'item':item}
                        )
        #列表页翻页
        next_url_lst = re.findall(r'<a href=(.*?) class="next pagination-item',response.text,re.S)
        next_url = next_url_lst[0] if len(next_url_lst)>0 else None
        print('\r\nnext_url------------->\r\n',next_url)
        #next_url = response.xpath('//a[@text="下一页"]/@href').extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url,next_url)
            yield scrapy.Request(
                    next_url,
                    callback=self.parse,
                    )


    def parse_detail(self,response):
        item = response.meta['item']
        #if "img_list" not in item:
        #item["img_list"] = response.xpath('//img[@class="BOE_Image"]/@src').extract()
        #else:
        item["img_list"].extend(response.xpath('//img[@class="BDE_Image"]/@src').extract())
        next_url = response.xpath('//a[@text="下一页"]/@href').extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url,next_url)
            yield scrapy.Request(
                    next_url,
                    callback=self.parse_detail,
                    meta={'item':item}
                    )

        else:
            #print("parse_detail->",item)
            yield item
