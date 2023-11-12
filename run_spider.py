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

from temp import set

if __name__ == '__main__':

    mode = set.set()['mode']
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    mode_to_spider = {
        'user': UserSpider,
        'tweet_by_user_id': TweetSpiderByUserID,
        'tweet_by_keyword': TweetSpiderByKeyword,


        # 'comment': CommentSpider,
        # 'tweet_by_tweet_id': TweetSpiderByTweetID,
        # 'fan': FanSpider,
        # 'follow': FollowerSpider,
        # 'repost': RepostSpider,
    }
    process.crawl(mode_to_spider[mode])
    # the script will block here until the crawling is finished
    process.start()