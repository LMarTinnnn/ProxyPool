from v3.sql_command.sql_command import IpDatabase
from v3.config import config
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
        # 加一个去重复功能
        self.seen = []

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
                # 检测是否挂上代理
                if remote_info != self.local_info:
                    # 去重复～
                    if host not in self.seen:
                        print('[Checker]: [%s] this works~' % ip)
                        self.seen.append(host)
                    else:
                        print('[Checker]: [%s] duplicated' % ip)
                        self.db.delete(host)
                        self.db.insert((host, port))   # 因为sql的delete操作会删除掉所有相同项 所以要再加上去。。。 感觉好蠢
                else:
                    print('[Checker]: [%s] invalid ip ... check another one' % ip)
                    self.db.delete(host)
            # Timeout or Max Retries exceptions
            except:
                print('[Checker]: [%s] timeout ... check another one' % ip)
                self.db.delete(host)

    def run(self):
        self.check()

if __name__ == '__main__':
    c = Checker()
    while True:
        c.run()
        print('休息30分钟')
        sleep(config.pause_time_check)
