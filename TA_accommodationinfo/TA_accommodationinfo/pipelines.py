# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import datetime
import sys
sys.path.insert(0, "C:/Users/mkind/PycharmProjects/TripAdvisor_scrapers_2022/Input_directory")

from Input_file import input_database, input_url


class TaAccommodationinfoPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient("localhost", 27017)
        database = self.conn[input_database]
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        location = input_url.split("-")[2]
        self.collection = database[f"Accommodations/{location}/{date}"]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
