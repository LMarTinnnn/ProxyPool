from IP_Pool.v3.sql_command.sql_command import IpDatabase
from IP_Pool.v3.config import config
import requests
from time import sleep


def local_info():
    """返回当前ip的地址信息"""
    page = requests.get(config.test_url, headers=config.headers)
    return page.text


class Checker(object):
    def __init__(self):
        self.db = IpDatabase()
        self.local_info = local_info()

    def check(self):
        print('[Checker]: 开始检查ip有效性...')
        ips = self.db.get()

        while not ips:
            print('[Checker]: 等待ip_crawler爬取代理信息...')
            sleep(config.pause_time_pool)
            ips = self.db.get()

        for host, port in ips:
            ip = '%s:%s' % (host, port)
            try:
                proxy = dict(http='http://' + ip)
                remote_info = requests.get(config.test_url, config.headers, proxies=proxy, timeout=3).text
                if remote_info != self.local_info:
                    print('[Checker]: [%s] this works~' % ip)
                else:
                    print('[Checker]: [%s] invalid ip ... check another one' % ip)
                    self.db.delete(host)
            except:
                print('[Checker]: [%s] timeout ... check another one' % ip)
                self.db.delete(host)
        self.db.commit()

    def run(self):
        self.check()

if __name__ == '__main__':
    c = Checker()
    while True:
        c.run()
        print('休息30分钟')
        sleep(config.pause_time_check)
