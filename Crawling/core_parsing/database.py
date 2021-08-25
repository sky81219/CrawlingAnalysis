import pymysql
from pymongo import MongoClient

class MysqlConnect:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', charset='utf8', db='url_site')

    def url_status_db_insert(self, url, status, title, a_tag):
        try:
            # insert
            sql_query = "INSERT INTO url_status (url, status_code, title, a_tag) VALUE  (%s, %s, %s, %s)"
            self.conn.cursor().execute(sql_query, (url, status, title, a_tag))
        finally:
            print('save finish')
            self.conn.close()

    def url_tag_db_insert(self, url, a_tag, href_tag, text_tag):
        try:
            sql_query = "INSERT INTO url_tag (url, a_tag, href_tag, text_tag) VALUE (%s, %s, %s, %s)"
            self.conn.cursor().execute(sql_query, (url, a_tag, href_tag, text_tag))
        finally:
            print('save finish')
            self.conn.close()

class MongoDbManager:
    def __init__(self, loot, port):
        self.instance = None
        self.client = MongoClient(loot, port)
