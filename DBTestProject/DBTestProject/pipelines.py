# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3

class DbtestprojectPipeline:
    def process_item(self, item, spider):
        return item

class WordsPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('word_counts.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_counts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host TEXT NOT NULL,
                word_count INTEGER NOT NULL,
                words TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute('''
                INSERT INTO word_counts (host, word_count, words) VALUES (?, ?, ?)
            ''', (item['host'], item['word_count'], item['words']))
            self.connection.commit()
        except sqlite3.Error as e:
            spider.log(f"Failed to insert item: {e}", level=scrapy.log.ERROR)
        return item