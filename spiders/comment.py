#!/usr/bin/env python

"""
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import json
from scrapy import Spider
from scrapy.http import Request
from spiders.common import parse_user_info, parse_time, url_to_mid
import sys
s = eval(sys.argv[2])




import logging

class CommentSpider(Spider):
    """
    微博评论数据采集
    """
    name = "comment"

    def start_requests(self):
        """
        爬虫入口
        """
        # 这里tweet_ids可替换成实际待采集的数据
        # print('sys.argv', sys.argv)

        tweet_ids = [s['keywords']]
        for tweet_id in tweet_ids:
            mid = url_to_mid(tweet_id)
            logging.info("mid: %s", mid)
            logging.info("tweet_id: %s", tweet_id)
            url = f"https://weibo.com/ajax/statuses/buildComments?" \
                  f"is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count=20"
            yield Request(url, callback=self.parse, meta={'source_url': url})

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        # print('!!!!!!!!!!!!!!!!!!!!data!!!!!!!!!!!!!!!!!!', data)
        # print('!!!!!!!!!!!!!!!!!!!!data!!!!!!!!!!!!!!!!!!', response.text)
        for comment_info in data['data']:
            item = self.parse_comment(comment_info)
            yield item
        if data.get('max_id', 0) != 0:
            url = response.meta['source_url'] + '&max_id=' + str(data['max_id'])
            yield Request(url, callback=self.parse, meta=response.meta)

    @staticmethod
    def parse_comment(data):
        """
        解析comment
        """
        item = dict()
        item['created_at'] = parse_time(data['created_at'])
        item['_id'] = data['id']
        item['like_counts'] = data['like_counts']
        if 'source' in data:
            item['ip_location'] = data['source']
        else:
            item['ip_location'] = None
        item['content'] = data['text_raw']
        item['comment_user'] = parse_user_info(data['user'])
        return item
