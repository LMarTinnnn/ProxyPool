import requests
import pickle
with open('pool.txt', 'rb') as file:
    ips = pickle.load(file)

print(len(ips))


def check_ip(ips):
    for proxy in ips:
        proxies = dict(http='http://' + proxy)
        try:
            res = requests.get('http://ip.chinaz.com/getip.aspx', proxies=proxies, timeout=3)
            print(res.text)
            if '河南' in res.text:
                print('[%s] not valid' % proxy)
                ips.remove(proxy)
                continue
        except:
            print('[%s] not valid' % proxy)
            ips.remove(proxy)
            continue

check_ip(ips)