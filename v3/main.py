import threading
from time import sleep

import config
from ip_pool.checker import Checker
from ip_pool.ip_crawler import IpCrawler


def crawler():
    i = IpCrawler(ip_number=20)
    try:
        while True:
            i.run()
            print('{Crawler}: sleep for 15 minutes')
            sleep(config.pause_time_pool)
    except KeyboardInterrupt:
        i.db.close()


def checker():
    c = Checker()
    try:
        while True:
            c.run()
            print('[Checker]: sleep for 30 minutes')
            sleep(config.pause_time_check)
    except KeyboardInterrupt:
        c.db.close()


def main():
    threading.Thread(target=crawler, args=()).start()
    threading.Thread(target=checker, args=()).start()


if __name__ == '__main__':
    main()
