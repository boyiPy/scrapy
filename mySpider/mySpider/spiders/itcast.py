import scrapy
import logging

logger = logging.getLogger(__name__)
class ItcastSpider(scrapy.Spider):
    name = 'itcast'#爬虫名
    allowed_domains = ['itcast.cn']#允许爬去的范围
    start_urls = ['https://www.itcast.cn/channel/teacher.shtml']#起始爬去的url

    def parse(self, response):#处理start_urls响应
        #resp = response.xpath('//div[@class="maincon"]//h3/text()').extract()
        #print(resp)
        #分组
        li_list = response.xpath('//div[@class="maincon"]//li')
        for li in li_list:
            item = {}
            item["name"] = li.xpath(".//div[@class='main_mask']/h2/text()").extract()[0]
            item["year"] = li.xpath(".//div[@class='main_mask']/h3/text()").extract()[0]
            item["introduce"] = li.xpath(".//div[@class='main_mask']/p/text()").extract_first()
            #print(item)
            logger.warning(item)
            yield item
