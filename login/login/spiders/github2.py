import scrapy
import re

class Github2Spider(scrapy.Spider):
    name = 'github2'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
                response,#自动从response中寻找form表单
                formdata={'login':'boyiPy','password':'691257chen'},
                callback=self.after_login
                )
    def after_login(self,response):
        print(re.findall("boyiPy",response.body.decode()))
