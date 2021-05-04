import scrapy


class Luffy173Spider(scrapy.Spider):
    name = 'luffy173'
    allowed_domains = ['book.apeland.cn']
    start_urls = ['http://book.apeland.cn/details/12/']

    def parse(self, response):
        print(response.text)
        content = response.xpath('//div[@class="book-content"]//text()').extract()
        print("--------------",content)
        print(response.request.headers("User-Agent"))
