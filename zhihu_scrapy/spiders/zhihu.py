# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from zhihu_scrapy.items import UserItem


class ZhihuSpider(scrapy.Spider):

    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    # 获取指定url_token的用户的详细信息
    user_info_url = ('https://www.zhihu.com/api/v4/members/{user}?'
                     'include={include}')
    # 获取该用户关注的用户的信息
    followees_url = ('https://www.zhihu.com/api/v4/members/{user}'
                     '/followees?include={include}&amp;'
                     'offset={offset}&amp;limit={limit}')
    # 获取关注该用户的用户的信息
    followers_url = ('https://www.zhihu.com/api/v4/members/{user}'
                     '/followers?include={include}&amp;'
                     'offset={offset}&amp;limit={limit}')
    # 初始爬取的用户url_token
    start_user_url_token = 'zhang-jia-wei'
    # 获取用户详细信息的查询字段
    user_query = ('locations,employments,gender,educations,business,'
                  'voteup_count,thanked_Count,follower_count,following_count,'
                  'cover_url,following_topic_count,following_question_count,'
                  'following_favlists_count,following_columns_count,'
                  'answer_count,articles_count,pins_count,question_count,'
                  'commercial_question_count,favorite_count,favorited_count,'
                  'logs_count,marked_answers_count,marked_answers_text,'
                  'message_thread_token,account_status,is_active,'
                  'is_force_renamed,is_bind_sina,sina_weibo_url,'
                  'sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,'
                  'is_following,is_followed,mutual_followees_count,'
                  'vote_to_count,vote_from_count,thank_to_count,'
                  'thank_from_count,thanked_count,description,'
                  'hosted_live_count,participated_live_count,'
                  'allow_message,industry_category,org_name,'
                  'org_homepage,badge[?(type=best_answerer)].topics')
    # 获取该用户关注的用户的信息的查询字段
    followees_query = ('data[*].answer_count,articles_count,gender,'
                       'follower_count,is_followed,is_following,'
                       'badge[?(type=best_answerer)].topics')
    # 获取关注该用户的用户的信息的查询字段
    followers_query = ('data[*].answer_count,articles_count,gender,'
                       'follower_count,is_followed,is_following,'
                       'badge[?(type=best_answerer)].topics')

    # def parse(self, response):# TODO 加入这个方法不实现逻辑会不会出错
    #     pass

    def start_requests(self):
        """初始请求

        :return:
        """
        yield Request(self.user_info_url.format(user=self.start_user_url_token,
                                                include=self.user_query),
                      self.parse_user_info)
        yield Request(self.followees_url.format(user=self.start_user_url_token,
                                                include=self.followees_query,
                                                limit=20, offset=0),
                      self.parse_followees)
        yield Request(self.followers_url.format(user=self.start_user_url_token,
                                                include=self.followers_query,
                                                limit=20, offset=0),
                      self.parse_followers)

    def parse_user_info(self, response):
        """查询用户详细信息的回调函数

        :param response:
        :return:
        """
        result = json.loads(response.text)
        user_item = UserItem()

        for field in user_item.fields:
            if field in result.keys():
                user_item[field] = result.get(field)
        yield user_item

        yield Request(
            self.followees_url.format(user=result.get('url_token'),
                                      include=self.followees_query,
                                      limit=20, offset=0),
            self.parse_followees)

        yield Request(
            self.followers_url.format(user=result.get('url_token'),
                                      include=self.followers_query,
                                      limit=20, offset=0),
            self.parse_followers)

    def parse_followees(self, response):
        """查询关注列表的回调函数

        :param response:
        :return:
        """
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(
                    self.user_info_url.format(user=result.get('url_token'),
                                              include=self.user_query),
                    self.parse_user_info)

        if 'paging' in results.keys():
            if results.get('paging').get('is_end') is False:
                next_page = results.get('paging').get('next')
                yield Request(next_page, self.parse_followees)

    def parse_followers(self, response):
        """查询关注者列表的回调函数

        :param response:
        :return:
        """
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(
                    self.user_info_url.format(user=result.get('url_token'),
                                              include=self.user_query),
                    self.parse_user_info)

        if 'paging' in results.keys():
            if results.get('paging').get('is_end') is False:
                next_page = results.get('paging').get('next')
                yield Request(next_page,
                              self.parse_followers)
