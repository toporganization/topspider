# -*- coding: utf-8 -*-
from scrapy import log
from scrapy import signals
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MysqlStoreNewsPipline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', 
                host = '',
                db = 'topspider',
                user = 'root',
                passwd = '',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = True
                )

    #pipline 默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._do_upinsert, item)
        query.addErrback(self._handle_error)
        return item

    #写入数据库
    def _do_upinsert(self, conn, item):

        conn.execute('insert into news(`title`,`content`) values("%s", "%s")',
                (item['title'], item['content']))

    #异常处理
    def _handle_error(self, failure):
        log.err(failure)



