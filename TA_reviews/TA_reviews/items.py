# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaReviewsItem(scrapy.Item):
    # define the fields for your item here like:

    location_id = scrapy.Field()
    location_name = scrapy.Field()

    review_creationDate = scrapy.Field()
    review_publishedDate = scrapy.Field()

    review_rating = scrapy.Field()

    review_subratings = scrapy.Field()

    review_publishedPlatform = scrapy.Field()

    review_title = scrapy.Field()
    review_text = scrapy.Field()
    review_roomTip = scrapy.Field()
    review_language = scrapy.Field()
    review_photos = scrapy.Field()

    review_stayDate = scrapy.Field()
    review_tripType = scrapy.Field()

    review_helpfulvotes = scrapy.Field()
    review_collected_by_TA = scrapy.Field()

    reviewer_username = scrapy.Field()
    reviewer_TA_page = scrapy.Field()
    reviewer_hometown = scrapy.Field()
    reviewer_posted_reviews_history = scrapy.Field()
    reviewer_received_likes_history = scrapy.Field()

    review_managementresponse_language = scrapy.Field()
    review_managementresponse_text = scrapy.Field()
    review_managementresponse_publishedDate = scrapy.Field()
    review_managementresponse_username = scrapy.Field()

    pass
