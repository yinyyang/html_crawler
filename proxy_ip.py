
import scrapy
from scrapy import Request


BSAE_URL='https://www.kuaidaili.com/free/inha/'
MEANING_URL =''
class ipSpider(scrapy.Spider):

    name = "ip_spider"
    start_urls = []
    for i in range(2):
        start_urls.append(BSAE_URL+str(i)+"/")



    def parse(self, response):
        # open_in_browser(response)
        SET_SELECTOR = '.content .con-body .table'
        # yield {
        #     "text": response.css(SET_SELECTOR).get()
        # }

        for wordEl in response.css(SET_SELECTOR):

            yield {
                "ip": wordEl.xpath('tbody//tr//td[@title="IP"]/text()').get(),
                "port": wordEl.xpath('tbody//tr//td[@title="IP"]/text()').get(),

            }



