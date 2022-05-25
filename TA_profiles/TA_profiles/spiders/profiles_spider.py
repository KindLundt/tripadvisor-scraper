import scrapy
from pymongo import MongoClient
import sys
import pandas
import json
from ..items import TaProfilesItem
import chompjs

sys.path.insert(0, "C:/Users/mkind/PycharmProjects/TripAdvisor_scrapers_2022/Input_directory")

from Input_directory.Input_file import input_database, profile_filter

class profile_spider (scrapy.Spider):
    name = "profile_spider"

    def start_requests(self):
        client = MongoClient()
        db = client[input_database]
        collection = db[profile_filter]
        data = pandas.DataFrame(list(collection.find()))

        for document in data.reviewer_TA_page:
            if document is not None:
                yield scrapy.Request(url=document, callback=self.parse)
            else:
                pass

    def parse(self, response, **kwargs):

        def nested_key_grabber(key, obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == key:
                        yield v
                    else:
                        yield from nested_key_grabber(key, v)
            elif isinstance(obj, list):
                for v in obj:
                    yield from nested_key_grabber(key, v)

        try:
            resp = response.xpath("//script[contains(.,'requests')]/text()").extract_first()
            access_json = chompjs.parse_js_object(resp)
            access_json = json.dumps(access_json)
            access_json = json.loads(access_json)

            urql_json = next(nested_key_grabber('urqlCache', access_json))
            urql_json_dump = json.dumps(urql_json)
            urql_json_loads = json.loads(urql_json_dump)
            urql_json_dump_again = json.dumps(urql_json_loads)

            clean_access_json = urql_json_dump_again.replace("\\\\n", " ") \
                .replace('\\\\"', "'") \
                .replace("\\", "") \
                .replace(' "{', '{') \
                .replace('}"},', '}},') \
                .removesuffix('"}}')
            clean_access_json_with_suffix = clean_access_json + "}}"

            fully_restored_json = json.loads(clean_access_json_with_suffix)
        except Exception as e:
            print(f"Error in Json {e}")


################
        username = next(nested_key_grabber("username", fully_restored_json))
        reviews = []
        for review in next(nested_key_grabber("sections", fully_restored_json)):
            if review["type"] == "REVIEW":
                one_review ={}
                one_review.update({"Title": review["items"][0]["object"]["title"]})
                one_review.update({"Text": review["items"][0]["object"]["text"]})
                one_review.update({"language": review["items"][0]["object"]["language"]})
                one_review.update({"publishedDate": review["items"][0]["object"]["publishedDate"]})
                one_review.update({"review_rating": review["items"][0]["object"]["rating"]})
                one_review.update({"location_name": review["items"][0]["object"]["location"]["name"]})
                one_review.update({"location_id": review["items"][0]["object"]["location"]["locationId"]})
                one_review.update({"location_type": review["items"][0]["object"]["location"]["placeType"]})
                one_review.update({"location_town": review["items"][0]["object"]["location"]["parent"]["additionalNames"]["long"]})
                one_review.update({"location_rating": review["items"][0]["object"]["location"]["reviewSummary"]["rating"]})
                one_review.update({"location_rating_count": review["items"][0]["object"]["location"]["reviewSummary"]["count"]})
                one_review.update({"location_name": review["items"][0]["object"]["location"]["name"]})


                reviews.append(one_review)
            else:
                pass




        if next(nested_key_grabber("hasMore", fully_restored_json)) is True:


                loady = yield scrapy.Request(url="https://www.tripadvisor.com/data/graphql/ids",
                                          method="POST",
                                          headers={"content-type": "application/json"})

                print("this is load_more:", loady)



###############
        items = TaProfilesItem()

        items["reviews"] = reviews
        items["username"] = username
        yield items
