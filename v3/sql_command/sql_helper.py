import sqlite3
import os
import sys

db_name = 'db_ip_pool'
relative_path = '/../data/%s' % db_name
fields = ('ip', 'port')


class IpDatabase(object):
    def __init__(self):
        self.table_name = 'ip_pool'
        self.absolute_db_path = os.path.dirname(sys.argv[0]) + relative_path
        self.conn = sqlite3.connect(self.absolute_db_path)
        self.cur = self.conn.cursor()
        self.create()

    def create(self):
        sql_create = 'CREATE TABLE IF NOT EXISTS %s (ip TEXT, port TEXT)' % self.table_name
        self.cur.execute(sql_create)

    def insert(self, proxy_list):
        sql_insert = 'INSERT INTO ip_pool VALUES (?,?)'
        # 如果没传list
        if isinstance(proxy_list, tuple):
            self.cur.execute(sql_insert, proxy_list)
        else:
            self.cur.executemany(sql_insert, [(ip, port) for ip, port in proxy_list])
        # print('rowcount: ', self.cur.rowcount)
        self.conn.commit()

    def delete(self, ip):
        sql_delete = 'DELETE FROM %s WHERE ip=?' % self.table_name
        data = (ip,)
        self.cur.execute(sql_delete, data)
        # print('rowcount: ', self.cur.rowcount)
        self.conn.commit()

    def get(self, number=None):
        sql_select = 'SELECT * FROM %s' % self.table_name
        self.cur.execute(sql_select)
        if number:
            return [(ip, port) for ip, port in self.cur.fetchmany(number)]
        else:
            return [(ip, port) for ip, port in self.cur.fetchall()]

    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    i = IpDatabase()
    i.insert(('123.0.0.0', '000'))
