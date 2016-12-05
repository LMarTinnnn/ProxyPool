import requests
import os
import pickle
from IP_Pool.ProxiesFounder import ProxiesFounder


class ProxiesChecker(object):
    def __init__(self):
        self.file_path = os.getcwd()
        self.ip_port_list = self.load_list()
        self.valid_ip = []

    def load_list(self):
        with open(os.path.join(self.file_path, 'ip.txt'), 'rb') as file:
            return pickle.load(file)

    def run(self):
        for proxy in self.ip_port_list:
                proxies = dict(http='http://' + proxy)

                try:
                    res = requests.get('http://ip.chinaz.com/getip.aspx', proxies=proxies, timeout=0.5)
                    print(res.text)
                    if '河南' in res.text:
                        print('[%s] not valid' % proxy)
                        continue
                    self.valid_ip.append(proxy)

                except:
                    print('[%s] not valid' % proxy)
                    continue
        # remove the invalid ip
        with open(os.path.join(self.file_path, 'valid_ip.txt'), 'wb') as file:
            pickle.dump(self.valid_ip, file)

if __name__ == '__main__':
    ProxiesFounder().run()
    C = ProxiesChecker()
    C.run()

