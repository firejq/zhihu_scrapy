# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

import requests
import time
from bs4 import BeautifulSoup
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        try:
            proxy_ip = self.get_proxy_ip()
            print('获取到代理ip：' + proxy_ip)
            request.meta['proxy'] = proxy_ip
        except Exception as error:
            print(error)

    def initial_proxies_pool(self):
        """爬取http://www.xicidaili.com/nn/首页的高匿代理ip

        :return: 可用的代理ip
        """
        headers = {
            'User-Agent': RandomUserAgentMiddleware.get_random_useragent()
        }
        url = 'http://www.xicidaili.com/nn/'
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        # ip_list为可用的代理ip列表
        # ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            protocol = 'https' if 'HTTPS' in tds[5].text else 'http'
            proxy_uri = protocol + '://' + tds[1].text + ':' + tds[2].text
            if self.verify_proxy(proxy_uri):
                # ip_list.append(proxy_uri)
                with open('proxies.txt', 'a') as f:
                    f.write(proxy_uri + '\n')
                    print('写入:' + proxy_uri)

    def get_proxy_ip(self):
        """随机从文件中读取proxy"""
        while True:
            with open('proxies.txt', 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)
        while True:
            proxy_ip = random.choice(proxies).strip()
            if self.verify_proxy(proxy_ip):
                return proxy_ip
        # return ''.join(str(random.choice(ip_list)).strip())

    @staticmethod
    def verify_proxy(proxy_ip):
        if proxy_ip:
            protocol = 'https' if 'https' in proxy_ip else 'http'
            proxies = {protocol: proxy_ip}
            try:
                if requests.get(url='http://www.baidu.com', proxies=proxies,
                                timeout=2).status_code == 200:
                    print('success %s' % proxy_ip)
                    return True
                else:
                    return False
            except BaseException:
                print('fail %s' % proxy_ip)
                return False


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        # request.headers['User-Agent'] = get_random_useragent()
        request.headers.setdefault(
            'User-Agent', RandomUserAgentMiddleware.get_random_useragent()
        )

    @staticmethod
    def get_random_useragent():
        """返回一个随机user-agent
        :return:
        """
        user_agents = [
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/60.0.3072.0 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 '
             'Firefox/46.0'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,'
             ' like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 '
             '(KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 '
             'Edge/13.10586'),
            ('Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) '
             'like Gecko'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
             'like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
             'like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
             'like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 '
             'QQBrowser/9.4.7658.400'),
            ('Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) '
             'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
             'Chrome/37.0.0.0 Mobile Safari/537.36 '
             'MicroMessenger/6.0.2.56_r958800.520 NetType/WIFI'),
            ('Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) '
             'AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 '
             'QQ/5.2.1.302 NetType/WIFI Mem/28')
        ]
        return random.choice(user_agents)


if __name__ == '__main__':
    p = ProxyMiddleware()
    p.initial_proxies_pool()
    # print(p.get_proxy_ip())
