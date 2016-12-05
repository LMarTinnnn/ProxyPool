"""
  v2.0 IpPool
     # 1. align IpPool's 'save' parameter 'True' to create a 'pool.txt' to stored pickled ip
     2. IpPool(target_site_url, ip_number, foreign).give_me_ip() will return a list of valid ip
        e.g: ['http://host:port', 'http://host2:port2', .....]
"""

from bs4 import BeautifulSoup as Bs
import requests
import random
import re

_re_ip = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')

ua = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) "
    "Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
]


class IpPool(object):
    def __init__(self, target_site_url, *, ip_number=4, foreign=True):
        if foreign:
            self.url = 'http://www.xicidaili.com/wn/'
        else:
            self.url = 'http://www.xicidaili.com/nn/'

        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'}

        if 'http' not in target_site_url:
            target_site_url = 'http://' + target_site_url
        self.target_site = target_site_url
        self.ip_number = ip_number
        self.new_ip = self.get_ip()
        self.valid_ip = self.choose_valid_ip()

    def give_me_ip(self):
        # method to give you valid proxies list
        # [ ('ip:port'), ...... ]
        return self.valid_ip

    def get_ip(self):
        print('开始获取ip...')
        host_list = []
        port_list = []
        html = requests.get(self.url, headers=self.headers)
        soup = Bs(html.text, 'lxml')
        for i in soup.find_all(string=_re_ip):
            host_list.append(i)
            port_list.append(i.parent.next_sibling.next_sibling.string)
        ip = ['%s:%s' % (host, port) for host, port in zip(host_list, port_list)]
        return ip

    def choose_valid_ip(self):
        valid_ip = []
        for ip in self.new_ip:
            try:
                header = {'User-Agent': random.choice(ua)}

                proxy = {'http': 'http://' + ip}
                page = requests.get(self.target_site, allow_redirects=False, timeout=3, proxies=proxy,
                                    headers=header)
                print(ip)
                # print('THIS WORK')
                valid_ip.append('http://' + ip)
                if len(valid_ip) >= self.ip_number:
                    break
            except:
                print('[%s] not work ..... check another one' % ip)
        return valid_ip


if __name__ == '__main__':
    ips = IpPool('http://91.t9l.space/forumdisplay.php?fid=19&page=1', foreign=True).give_me_ip()
    print(ips)
    '''
    header = {'User-Agent': random.choice(ua),
              'Referer': 'https://www.douban.com/',
              'Host': 'book.douban.com'}
    cookies = {
        'cookie': '__ads_session=VPH0JhNv0wgn+j8uTwA=; domain=.douban.com; path=/'
    }
    page = requests.get('https://book.douban.com/subject/26895253/', timeout=2,
                        headers=header)
    print(page.status_code)'''
