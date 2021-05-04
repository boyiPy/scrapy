import scrapy


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['tencent.com']
    start_urls = ['https://careers.tencent.com/search.html']

    def parse(self, response):
        print(response.text)
        div_list = response.xpath('//div[@class="correlation-degree"]/div/div')
        for div in div_list:
            item = {}
            item["title"] = div.xpath('./a/h4/text()').extract_first()
            item['tip'] = div.xpath('./p[1]/text()').extract_first()
            item['text'] = div.xpath('./p[2]/text()').extract_first()
            yield item
