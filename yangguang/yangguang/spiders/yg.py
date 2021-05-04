import scrapy
from yangguang.items import YangguangItem

class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/search?keyword=%E6%8A%95%E8%AF%89&page=1']
    base_url = 'http://wz.sun0769.com'
    page_num = 2
    def parse(self, response):
        li_list = response.xpath('//ul[@class="title-state-ul"]/li')
        for li in li_list:
            item = YangguangItem()
            item['title'] = li.xpath('./span[3]/a/text()').extract_first()
            item['href'] = self.base_url + li.xpath('./span[3]/a/@href').extract_first()
            item['time'] = li.xpath('./span[4]/text()').extract_first()
            print(item)
            yield scrapy.Request(
                    item["href"],
                    callback=self.parse_detail,
                    meta={"item":item}
                    )

            #下一页
            next_url = self.base_url + response.xpath("//div[@class='mr-three paging-box']/a[2]/@href").extract_first()
            #由于网页没有跳转到最后一页，所以就先翻10页结束
            if self.page_num < 10:
                self.page_num += 1
                if next_url is not None:
                    yield scrapy.Request(
                            next_url,
                            callback=self.parse_next
                            )
    #没有响应到parse_detail,原因??：是还allowed_domains问题，末尾加了\
    def parse_detail(self, response):
        print(response.url)
        item = response.meta["item"]
        print('parse_detail',item)
        item['content'] = response.xpath('//div[@class="details-box"]//text()').extract()
        item['content_img'] = response.xpath('//div[@class="clear details-img-list Picture-img"]/@src').extract()
        #print(item)
        print("page_details-----------------\r\n")
        yield item
    def parse_next(self, response):
        print('next_page----------------\r\n')
