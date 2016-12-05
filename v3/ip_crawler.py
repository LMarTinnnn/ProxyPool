from IP_Pool.v3.sql_command.sql_command import IpDatabase
from IP_Pool.v3.config import config
import requests
from bs4 import BeautifulSoup as Bs
from time import sleep
import re

_re_ip = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')


def local_info():
    """返回当前ip的地址信息"""
    page = requests.get(config.test_url, headers=config.headers)
    return page.text


class IpCrawler(object):
    def __init__(self, *, ip_number=5, foreign=True):
        if foreign:
            self.url = 'http://www.xicidaili.com/wn/'
        else:
            self.url = 'http://www.xicidaili.com/nn/'
        self.ip_number = ip_number
        self.db = IpDatabase()
        self.local_info = local_info()

    def get_ip(self):
        """从目标网站获取代理"""
        print('{Crawler}: 开始获取ip...')
        host_list = []
        port_list = []
        html = requests.get(self.url, headers=config.headers)
        soup = Bs(html.text, 'lxml')
        for i in soup.find_all(string=_re_ip):
            host_list.append(i)
            port_list.append(i.parent.next_sibling.next_sibling.string)
        # ip = ['%s:%s' % (host, port) for host, port in zip(host_list, port_list)]
        # return ip
        ip_list = zip(host_list, port_list)
        return ip_list

    def valid_ip(self):
        """检测ip可用性"""
        ips = self.get_ip()
        valid_ip = []
        for host, port in ips:
            ip = '%s:%s' % (host, port)
            try:
                proxy = dict(http='http://' + ip)
                remote_info = requests.get(config.test_url, config.headers, proxies=proxy, timeout=3).text
                if remote_info != self.local_info:
                    print('{Crawler}: [%s] this works~' % ip)
                    valid_ip.append((host, port))
                else:
                    print('{Crawler}: [%s] invalid ip ... check another one' % ip)
                if len(valid_ip) >= self.ip_number:
                    break
            except:
                print('{Crawler}: [%s] timeout ... check another one' % ip)
        self.db.insert(valid_ip)
        self.db.commit()

    def run(self):
        self.valid_ip()

if __name__ == '__main__':
    test = IpCrawler(foreign=True, ip_number=30)
    while True:
        test.run()
        print('休息15分钟...')
        sleep(config.pause_time_pool)
