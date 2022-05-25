# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import datetime
from scrapy.exceptions import DropItem

import sys

sys.path.insert(0, "C:/Users/mkind/PycharmProjects/TripAdvisor_scrapers_2022")

from Input_directory.Input_file import input_url, input_database


class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['accommodation_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %r" % item)
        else:
            self.ids_seen.add(adapter['hotel_ids'])
            return item


class TaListingsPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient("localhost", 27017)
        database = self.conn[input_database]
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        location = input_url.split("-")[2]

        self.collection = database[f"Listings/{location}/{date}"]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
