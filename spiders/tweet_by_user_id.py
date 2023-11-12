#!/usr/bin/env python

"""
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import json
from scrapy import Spider
from scrapy.http import Request
from spiders.common import parse_tweet_info, parse_long_tweet
import sys
sys.path.append("..")
from temp import set
s = set.set()

class TweetSpiderByUserID(Spider):
    """
    用户推文数据采集
    """
    name = "tweet_spider_by_user_id"
    base_url = "https://weibo.cn"

    def start_requests(self):
        """
        爬虫入口
        """
        user_ids = [s['keywords']]
        # with open(s['keywords'], 'r') as f:
            # for line in f:
                # user_ids.append(line.strip())
        # print(user_ids)
        for user_id in user_ids:
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page=1"
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': 1})

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        tweets = data['data']['list']
        for tweet in tweets:
            item = parse_tweet_info(tweet)
            del item['user']
            if item['isLongText']:
                url = "https://weibo.com/ajax/statuses/longtext?id=" + item['mblogid']
                yield Request(url, callback=parse_long_tweet, meta={'item': item})
            else:
                yield item
        if tweets:
            user_id, page_num = response.meta['user_id'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page={page_num}"
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})
