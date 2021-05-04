import scrapy
import re


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']
    '''
    start_urls = ['https://github.com/boyiPy/boyiPy']
    def start_requests(self):
        直接使用cookies
        cookies = '_octo=GH1.1.93921716.1619441225; logged_in=yes; dotcom_user=boyiPy; color_mode={"color_mode":"auto","light_theme":{"name":"light","color_mode":"light"},"dark_theme":{"name":"dark","color_mode":"dark"}}; tz=Asia/Shanghai'
        cookies = {i.split('=')[0]:i.split('=')[1] for i in cookies.split(';')}
        yield scrapy.Request(
                self.start_urls[0],
                callback=self.parse,
                cookies=cookies
                )
        '''
    def parse(self, response):
        #cookies验证
        #print(re.findall(" Hi, I’m @boyiPy",response.body.decode()))
        authenticity_token = response.xpath('//input[@name="authenticity_token"]/@value').extract_first()
        commit = response.xpath('//input[@name="commit"]/@value').extract_first()
        post_data = dict(
            authenticity_token = authenticity_token,
            commit = commit,
            login = "boyiPy",
            password = '691257chen'
            )
        yield scrapy.FormRequest(
                'https://github.com/session',
                formdata=post_data,
                callback=self.after_login
                )

    def after_login(self,response):
        print(re.findall("boyiPy",response.body.decode()))
