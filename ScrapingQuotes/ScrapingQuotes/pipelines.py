# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class ScrapingquotesPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("quotes_collection")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("DROP TABLE IF EXISTS quotes_table")
        self.curr.execute("""CREATE TABLE quotes_table(
                            quote text,
                            author text,
                            tags text)""")

    def process_item(self, item, spider):
        self.store_to_database(item)
        return item

    def store_to_database(self, item):
        self.curr.execute("INSERT INTO quotes_table VALUES(?, ?, ?)",
                            (item['quote'][0],
                            item['author'][0],
                            item['tags'][0]))
        self.conn.commit()