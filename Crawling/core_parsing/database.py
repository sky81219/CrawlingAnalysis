import pymysql
from pymongo import MongoClient


class MysqlConnect:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', charset='utf8', db='url_site')
        self.cursor = self.conn.cursor()

    def url_status_db_insert(self, url, status, title, a_tag, link_tag):
        try:
            # insert
            sql_query = "INSERT INTO url_status (url, status_code, title, a_tag, link_tag) " \
                        "VALUE  (%s, %s, %s, %s, %s)"
            self.cursor.execute(sql_query, (url, status, title, a_tag, link_tag))
            return self.conn.commit()
        except pymysql.err.Error as e:
            print(e)

    def url_tag_db_insert(self, url, title, a_tag, a_href_tag, link_tag, link_href_tag):
        try:
            sql_query = "INSERT INTO url_tag " \
                        "(url, title, a_tag, a_href_tag, link_tag, link_href_tag) " \
                        "VALUE (%s, %s, %s, %s, %s, %s)"
            self.conn.cursor().execute(sql_query, (url, title, a_tag, a_href_tag, link_tag, link_href_tag))
            return self.conn.commit()
        except pymysql.err.Error as e:
            print(e)


class MongoDbManager:
    def __init__(self, loot, port):
        self.instance = None
        self.client = MongoClient(loot, port)


