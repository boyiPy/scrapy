import scrapy
from copy import deepcopy
import urllib

class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://vip.book.sina.com.cn/weibobook?pos=20002']
    book_total = 0
    def parse(self, response):
        #榜单大分类
        div_lst = response.xpath('//div[@class="lf_nav"]/div')
        for div in div_lst:
            item = {}
            item['b_cate'] = div.xpath('./h2/text()').extract_first().strip()
            #获取各大版
            li_lst = div.xpath('./div/ul/li')
            for li in li_lst:
                item['s_href'] = li.xpath('./a/@href').extract_first()
                item['s_cate'] = li.xpath('./a/text()').extract_first()
                if item['s_href'] is not None:
                    item['s_href'] = 'http://vip.book.sina.com.cn/' + item['s_href']
                yield scrapy.Request(
                        item['s_href'],
                        callback=self.parse_book_list,
                        meta = {'item':deepcopy(item)}
                        )

    #解析列表页
    def parse_book_list(self,response):
        item = response.meta['item']
        li_list = response.xpath('//div[@class="book_list"]//li')
        #print("book_list ->",len(li_list),'\n')
        for li in li_list:
            item['b_name'] = li.xpath('.//p[@class="book_name"]/a/text()').extract_first()
            item['b_href'] = li.xpath('.//p[@class="book_name"]/a/@href').extract_first()
            #print(item)
            if item['b_href'] is not None:
                item['b_href'] = urllib.parse.urljoin(response.url,item['b_href'])
            yield scrapy.Request(
                    item['b_href'],
                    callback=self.parse_detail,
                    meta = {'item':deepcopy(item)}
                    )
        #翻页
        next_url = response.xpath('//a[@text="下一页"]/@href').extract_first()
        if next_url is not'javascript:;':
            next_url = urllib.parse.urljoin(response.url,next_url)
            #print('next_url->',next_url)
            yield scrapy.Request(
                    next_url,
                    callback=self.parse_book_list
                    )



            
    #书页详情信息
    def parse_detail(self,response):
        item = response.meta['item']
        item['b_img'] = response.xpath('//div[@class="book_img"]/img/@src').extract_first()
        item['b_author'] = response.xpath('//div[@class="authorName"]/text()').extract_first().strip()
        item['b_sizeBit'] = response.xpath('//p[@class="sizeBit"]/text()').extract_first()
        item['b_state'] = response.xpath('//p[@class="static"]/text()').extract_first()
        item['b_words'] = ''.join(response.xpath('//div[@class="book_info_txt"]//text()').extract()).strip()
        print(item)
        self.book_total += 1
        print("crawl book total------->",self.book_total)
        print('-'*100,'\r\n')
