from bs4 import BeautifulSoup as bs
import requests
import pickle
import os


class ProxiesFounder(object):
    def __init__(self, file_path=os.getcwd()):
        self.file_path = file_path
        self.ip_port_list = self.load_list()

    def load_list(self):
        try:
            with open(os.path.join(self.file_path, 'ip.txt'), 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

    def get_ip(self):
        html = requests.get('http://haoip.cc/tiqu.htm').text
        soup = bs(html, 'lxml')
        ips = soup.find('div', class_="col-xs-12")
        for ip in ips.strings:
            if ip.strip() and ip.strip() not in self.ip_port_list:
                self.ip_port_list.append(ip.strip())

    def get_proxies(self):
        # return the (ip, port) list
        return list(self.ip_port_list)

    def run(self):
        # write the pickled (ip, port) list into ip.txt located in cwd
        self.get_ip()
        with open(os.path.join(self.file_path, 'ip.txt'), 'wb') as file:
            pickled_data = pickle.dumps(self.ip_port_list)
            # 为了不覆盖
            file.write(pickled_data)

if __name__ == '__main__':
    i = ProxiesFounder()
    i.run()
    print('请查看当前目录下 ip.txt 文件\nIf u wanna use the data ,do pickle.load()')
    print(len(i.ip_port_list))
