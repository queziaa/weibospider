#!/usr/bin/env python

"""
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2019-12-07 21:27
"""
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.tweet_by_user_id import TweetSpiderByUserID
from spiders.tweet_by_keyword import TweetSpiderByKeyword
from spiders.tweet_by_tweet_id import TweetSpiderByTweetID
from spiders.comment import CommentSpider
from spiders.follower import FollowerSpider
from spiders.user import UserSpider
from spiders.fan import FanSpider
from spiders.repost import RepostSpider
import sys

SET = eval(sys.argv[2])

if __name__ == '__main__':

    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    mode_to_spider = {
        'user': UserSpider,
        'tweet_by_user_id': TweetSpiderByUserID,
        'tweet_by_keyword': TweetSpiderByKeyword,
        'comment': CommentSpider,
        'fan': FanSpider,
        'follow': FollowerSpider,
        'repost': RepostSpider

        # 'tweet_by_tweet_id': TweetSpiderByTweetID,
    }
    process.crawl(mode_to_spider[SET['mode']],param1=sys.argv[1],param2=sys.argv[2],param3=sys.argv[3])
    process.start()