import random
from time import sleep

import proxy as proxy
import re

import scrapy
from scrapy import Request
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.utils import log

import pymysql

# Open database connection
from scrapy.utils.response import open_in_browser

db = pymysql.connect("localhost","word","123456","word" )
db.autocommit(True)
#
# # prepare a cursor object using cursor() method
cursor = db.cursor()


BSAE_URL='https://www.koolearn.com'
YOUDAO_URL ='http://www.youdao.com/w/eng/'
COLLINS_URL= 'https://www.collinsdictionary.com/dictionary/english-chinese/'
class wordSpider(scrapy.Spider):

    name = "word_spider"
    start_urls = []
    for i in range(19):
        start_urls.append(BSAE_URL+'/dict/tag_327_'+str(i+1)+'.html')
    print(start_urls)

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
            word = wordEl.xpath('text()').get()
            youdaoUrl = YOUDAO_URL+word
            collinsUrl = COLLINS_URL+word
            xdfUrl = BSAE_URL+ wordEl.xpath("@href").get()

            href = wordEl.xpath("@href").get()
            start = href.index('wd_')
            end = href.index('.html');
            word_idx=href[start+3:end]
            # self.logger.info(MEANING_URL)
            #sql = 'insert into word (word_idx,english)  values ('+word_idx+',"'+word+'")'
            #print(sql)
            #cursor.execute(sql)

            proxy_addr =random.choice(proxy.proxy_list)
            header = random.choice(proxy.user_agent_list)
           # yield Request(url = youdaoUrl,callback = self.parseMeaningYouDao,meta={'word_idx': word_idx})
            #yield Request(url=xdfUrl, callback=self.parseMeaning, meta={'word_idx': word_idx})
            yield Request(url=collinsUrl, callback=self.parseMeaningCollins, meta={'word_idx': word_idx})




    def parseMeaningYouDao(self, response):

        word_idx = response.meta.get('word_idx')
        print(word_idx)
        MEANING_SELECTOR = '.results-content .trans-wrapper'
        # yield {
        #       "meaning": response.css(MEANING_SELECTOR).get(),
        #   }
        leftcontentEl= response.css(MEANING_SELECTOR)
        content=leftcontentEl.css('.trans-container').get()
        soundmark = leftcontentEl.css('.baav .phonetic').get().replace("'","&apos")
        print(content)
        print(soundmark)
        # for a in content:
        #     print(a.xpath("text()").get())
        # print(content.find("'"))
        # if content.find("'")>0:
        #    newMeaning = content.replace("'","&apos")
        # else  :
        #    newMeaning = content
        #chinese = content
        #print(chinese)
        youdao_sql = "insert into word_ext (word_idx,youdao,soundmark)  values ("+word_idx+", '"+ re.escape(content) + "', '"+ re.escape(soundmark) + "')"
        print(youdao_sql)
        cursor.execute(youdao_sql)

    def parseMeaningCollins(self, response):
        word_idx = response.meta.get('word_idx')
        MEANING_SELECTOR = '.dictionary .res_cell_center .res_cell_center_content .he .cB'
        # yield {
        #       "meaning": response.css(MEANING_SELECTOR).get(),
        #   }
        centerEl= response.css(MEANING_SELECTOR)
        centerwordAreaEl=centerEl.xpath("div[3]")
        print(centerwordAreaEl.get())
        content = centerwordAreaEl.xpath('div[@class="hom"]')
        word='';
        for a in content:
            word = word+a.xpath("text()").get()
        print("word:"+word)

        word.replace("'", "&apos")
        sql = "update word_ext set collins = '" + re.escape(word) + "' where word_idx = " + word_idx + ""
        print(sql)
        cursor.execute(sql)

        # print(content.find("'"))
        # if content.find("'")>0:
        #    newMeaning = content.replace("'","&apos")
        # else  :
        #    newMeaning = content
        #chinese = content
        #print(chinese)
        #sql = "insert into word_ext (word_idx,chinese)  values (1,'"+ chinese + "')"
        #print(sql)
        #cursor.execute(sql)


    def parseMeaning(self, response):
        word_idx = response.meta.get('word_idx')
        print(word_idx)
        MEANING_SELECTOR = '.left-content .content-box'
        # yield {
        #       "meaning": response.css(MEANING_SELECTOR).get(),
        #   }
        leftcontentEl= response.css('.left-content')
        content = leftcontentEl.get().replace("'","&apos")
        print(content)
        # print(content.find("'"))
        # if content.find("'")>0:
        #    newMeaning = content.replace("'","&apos")
        # else  :
        #    newMeaning = content
        # chinese = leftcontentEl.xpath("div[@class='details-content-title-box']/div[1]").get()
        # sql = "insert into word_ext (word_idx,chinese)  values (" + word_idx + ",'"+ chinese + "')"
        if content:
            sql ="update word_ext set xdf = '"+re.escape(content)+"' where word_idx = "+word_idx+""
            print(sql)
            cursor.execute(sql)


#
# class RotateUserAgentMiddleware(UserAgentMiddleware):
#     def __init__(self, user_agent=''):
#         self.user_agent = user_agent
#
#     def process_request(self, request, spider):
#         ua = random.choice(self.user_agent_list)
#         if ua:
#             request.headers.setdefault('User-Agent', ua)
#
#             # Add desired logging message here.
#             spider.log(
#                 u'User-Agent: {} {}'.format(request.headers.get('User-Agent'), request),
#                 level=log.DEBUG
#             )

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php

