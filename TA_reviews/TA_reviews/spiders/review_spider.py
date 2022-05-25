import scrapy
from pymongo import MongoClient
import sys
import pandas
import json
from ..items import TaReviewsItem
import chompjs

sys.path.insert(0, "C:/Users/mkind/PycharmProjects/TripAdvisor_scrapers_2022")

from Input_directory.Input_file import input_database, select_accommodation_TYPE, reviews_filter


class review_spider (scrapy.Spider):
    name = "review_spider"

    def start_requests(self):
        client = MongoClient()
        db = client[input_database]
        collection = db[reviews_filter]
        data = pandas.DataFrame(list(collection.find()))

        filter_for_accommodation_type = data.loc[data["accommodation_type"] == select_accommodation_TYPE]

        for document in filter_for_accommodation_type.accommodation_url:
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

            clean_access_json = urql_json_dump_again.replace("\\\\n", " ")\
                .replace('\\\\"', "'")\
                .replace("\\", "") \
                .replace(' "{', '{')\
                .replace('}"},', '}},')\
                .removesuffix('"}}')
            clean_access_json_with_suffix = clean_access_json + "}}"

            fully_restored_json = json.loads(clean_access_json_with_suffix)
        except Exception as e:
            print(f"Error in Json {e}")



##################

        for review in next(nested_key_grabber("reviewListPage", fully_restored_json))["reviews"]:

            location_id = review["location"]["locationId"]
            location_name = review["location"]["name"]

            review_creationDate = review["createdDate"]
            review_publishedDate = review ["publishedDate"]

            review_rating = review["rating"]

            review_subratings = []
            for subrating in review["additionalRatings"]:
                item = {}
                item.update({"rating": subrating["rating"]})
                item.update({"rating_label": subrating["ratingLabel"]})
                review_subratings.append(item)

            review_publishedPlatform = review["publishPlatform"]

            review_title = review["title"]
            review_text = review["text"]
            review_roomTip = review["roomTip"]
            review_language = review["language"]
            review_photos = []
            for photo in review["photos"]:
                review_photos.append(photo["photoSizes"][-1]["url"])
            review_stayDate = review["tripInfo"]["stayDate"]
            review_tripType = review["tripInfo"]["tripType"]

            review_helpfulvotes = review["helpfulVotes"]

            review_collected_by_TA = review["provider"]["isLocalProvider"]

            reviewer_username = review["username"]
            reviewer_TA_page = "http://tripadvisor.com/" + review["userProfile"]["route"]["url"]

            try:
                reviewer_hometown = review["userProfile"]["hometown"]["location"]["additionalNames"]["long"]
            except TypeError:
                reviewer_hometown = review["userProfile"]["hometown"]["fallbackString"]

            reviewer_posted_reviews_history = review["userProfile"]["contributionCounts"]["sumAllUgc"]
            reviewer_received_likes_history = review["userProfile"]["contributionCounts"]["helpfulVote"]

            try:
                review_managementresponse_language = review["mgmtResponse"]["language"]
                review_managementresponse_text = review["mgmtResponse"]["text"]
                review_managementresponse_publishedDate = review["mgmtResponse"]["publishedDate"]
                review_managementresponse_username = review["mgmtResponse"]["username"]
            except TypeError:
                review_managementresponse_language = "N/A"
                review_managementresponse_text = "N/A"
                review_managementresponse_publishedDate = "N/A"
                review_managementresponse_username = "N/A"


################

            items = TaReviewsItem()

            items["location_id"] = location_id
            items["location_name"] = location_name
            items["review_creationDate"] = review_creationDate
            items["review_publishedDate"] = review_publishedDate
            items["review_rating"] = review_rating
            items["review_subratings"] = review_subratings
            items["review_publishedPlatform"] = review_publishedPlatform
            items["review_title"] = review_title
            items["review_text"] = review_text
            items["review_roomTip"] = review_roomTip
            items["review_language"] = review_language
            items["review_photos"] = review_photos
            items["review_stayDate"] = review_stayDate
            items["review_tripType"] = review_tripType
            items["review_helpfulvotes"] = review_helpfulvotes
            items["review_collected_by_TA"] = review_collected_by_TA
            items["reviewer_username"] = reviewer_username
            items["reviewer_TA_page"] = reviewer_TA_page
            items["reviewer_hometown"] = reviewer_hometown
            items["reviewer_posted_reviews_history"] = reviewer_posted_reviews_history
            items["reviewer_received_likes_history"] = reviewer_received_likes_history
            items["review_managementresponse_language"] = review_managementresponse_language
            items["review_managementresponse_text"] = review_managementresponse_text
            items["review_managementresponse_publishedDate"] = review_managementresponse_publishedDate
            items["review_managementresponse_username"] = review_managementresponse_username

            yield items

        next_page = response.css("a.next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


