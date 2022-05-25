# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaAccommodationinfoItem(scrapy.Item):
    # define the fields for your item here like:
    Front_photos = scrapy.Field()

    accommodation_name = scrapy.Field()
    accommodation_url = scrapy.Field()
    accommodation_type = scrapy.Field()
    location_coordinates = scrapy.Field()
    location_address = scrapy.Field()
    location_id = scrapy.Field()
    region_id = scrapy.Field()
    region_language = scrapy.Field()
    distance_unit = scrapy.Field()
    nearby_transit = scrapy.Field()
    nearby_airport = scrapy.Field()
    nearby_attractions_summary = scrapy.Field()
    walkScore_TA = scrapy.Field()
    nearby_locations_detail = scrapy.Field()
    accommodation_languages = scrapy.Field()
    accommodation_stars = scrapy.Field()
    star_rating_provider = scrapy.Field()
    overall_rating = scrapy.Field()
    overall_rating_count = scrapy.Field()
    subratings = scrapy.Field()
    property_amenities = scrapy.Field()
    room_features = scrapy.Field()
    room_types = scrapy.Field()
    green_leaders_level = scrapy.Field()
    travelers_choice_award = scrapy.Field()
    front_photos = scrapy.Field()

    currency_used = scrapy.Field()
    main_offers = scrapy.Field()
    textlink_offers = scrapy.Field()
    hidden_offers = scrapy.Field()
    price_percentiles_USD_cent = scrapy.Field()
    price_USD_cent_future = scrapy.Field()

    pass
