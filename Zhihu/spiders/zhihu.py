# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy import Request
from items import ZhihuItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    star_user = 'kaifulee'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/api/v4/members/kaifulee/followers?include=data%5B*%5D.answer_count%2Carticles'+ \
                  '_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20']


    def parse(self, response):
        result = json.loads(response.text)
        user = re.findall(r'members/(.*?)/followers',result['paging']['previous'])[0]
        for i in range(0,result['paging']['totals'],20):
            every_page_url = 'https://www.zhihu.com/api/v4/members/'+ user +'/followers?include=data%5B*%5D.answe' + \
                             'r_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B' + \
                             '%3F(type%3Dbest_answerer)%5D.topics&offset='+str(i)+'&limit=20'
            yield Request(every_page_url,self.parse_followers)


    def parse_followers(self,response):
        item = ZhihuItem()
        result = json.loads(response.text)
        data = result['data']
        for follower in data:
            item['name'] = follower['name']
            item['url'] = follower['url']
            item['gender'] = follower['gender']
            item['follower_count'] = follower['follower_count']
            item['articles_count'] = follower['articles_count']
            item['answer_count'] = follower['answer_count']
            item['headline'] = follower['headline']
            item['is_vip'] = follower['vip_info']['is_vip']
            yield item
            if follower['follower_count']:
                yield Request('https://www.zhihu.com/api/v4/members/'+ follower['url_token'] +'/followers?include=data%5B*%5D.answer_count%2Ca'
                              'rticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbe'
                              'st_answerer)%5D.topics&offset=0&limit=20',self.parse)

