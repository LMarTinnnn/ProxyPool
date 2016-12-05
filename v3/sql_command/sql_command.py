import sqlite3
import os


class IpDatabase(object):
    def __init__(self):
        self.db_name = 'db_ip_pool'
        self.db_dir = os.path.join('./data', self.db_name)
        self.table_name = 'ip_pool'
        self.fields = ('ip', 'port')
        self.conn = sqlite3.connect(self.db_dir)
        self.cur = self.conn.cursor()
        self.create()

    def create(self):
        sql_create = 'CREATE TABLE IF NOT EXISTS %s (ip TEXT, port TEXT)' % self.table_name
        self.cur.execute(sql_create)

    def insert(self, proxy_list):
        sql_insert = 'INSERT INTO ip_pool VALUES (?,?)'
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

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
