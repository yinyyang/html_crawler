import random
from time import sleep

import scrapy
from scrapy import Request
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.utils import log

import pymysql

# Open database connection
db = pymysql.connect("localhost","word","123456","word" )

# prepare a cursor object using cursor() method
cursor = db.cursor()


BSAE_URL='https://www.koolearn.com'
MEANING_URL =''
class wordSpider(scrapy.Spider):

    name = "word_spider"
    start_urls = [BSAE_URL+'/dict/tag_327_1.html',BSAE_URL+'/dict/tag_327_2.html']

    def parse(self, response):
        # open_in_browser(response)
        SET_SELECTOR = '.left-content .word-box .word'
        # yield {
        #     "text": response.css(SET_SELECTOR).get()
        # }
        for wordEl in response.css(SET_SELECTOR):
            NAME_SELECTOR = '.word'
            yield {
                "el": wordEl.css(NAME_SELECTOR).get(),
                "text": wordEl.xpath('text()').get(),
                "url": wordEl.xpath("@href").get(),

            }
            MEANING_URL = BSAE_URL+wordEl.xpath("@href").get()
            text = wordEl.xpath('text()').get()
            href = wordEl.xpath("@href").get()
            start = href.index('wd_')
            end = href.index('.html');
            word_idx=href[start+3:end]
            # self.logger.info(MEANING_URL)
            sql = 'insert into word (word_idx,english)  values ('+word_idx+',"'+text+'")'
            print(sql)
            cursor.execute(sql)

            yield Request(url = MEANING_URL,callback = self.parseMeaning,dont_filter=True)

        db.commit()
        db.close()
    def parseMeaning(self, response):
        url = response.url
        start = url.index('wd_')
        end = url.index('.html');
        word_idx = url[start + 3:end]
        MEANING_SELECTOR = '.left-content .content-box'
        # yield {
        #       "meaning": response.css(MEANING_SELECTOR).get(),
        #   }
        leftcontentEl= response.css('.left-content')
        content = leftcontentEl.xpath("div[3]").get()
        # print(content.find("'"))
        # if content.find("'")>0:
        #    newMeaning = content.replace("'","&apos")
        # else  :
        #    newMeaning = content
        chinese = leftcontentEl.xpath("div[@class='details-content-title-box']/div[1]").get()
        sql = "insert into word_ext (word_idx,chinese)  values (" + word_idx + ",'"+ chinese + "')"
        print(sql)
        cursor.execute(sql)



class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

            # Add desired logging message here.
            spider.log(
                u'User-Agent: {} {}'.format(request.headers.get('User-Agent'), request),
                level=log.DEBUG
            )

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
