import scrapy

import json
from ..items import TaAccommodationinfoItem
import chompjs
import sys

sys.path.insert(0, "C:/Users/mkind/PycharmProjects/TripAdvisor_scrapers_2022/Input_directory")
from Input_file import input_url


class accommodation_spider(scrapy.Spider):
    name = "accommodation_spider"
    start_urls = [input_url]

    # The accommodation_spider uses url scraped by the listings_spider. Accommodation spider asks the input_file for
    # the url from the most recent relevant listings_spider run (read more on this in the input_file). The spider then
    # establishes a connection with the collection and stores the data in a DataFrame to work on it.

    def parse(self, response, **kwargs):
        for link in response.css(".listing_title a::attr(href)"):
            yield response.follow(link.get(), callback=self.parse_accommodations)

        next_page = response.css("a.next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    def parse_accommodations(self, response, **kwargs):

        # The following function is used to run through the json-tree of a given json-object and search it for a given
        # key and return its corresponding value.
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

        # We access the downloaded page file and search for the pageManifest script to isolate it and
        # transform it into a json file.

        resp = response.xpath("//script[contains(.,'requests')]/text()").extract_first()
        access_json = chompjs.parse_js_object(resp)
        access_json = json.dumps(access_json)
        access_json = json.loads(access_json)

        # Within the json file we search for the subsection "urqlCache" - there the relevant data is stored.
        # The json file contains further nested json-files which however are "stringify"-ed, thus made into
        # strings containing expressions that need to be cleaned in order to be processed as a normal json-file.

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


#########################
        # Now that the json-file is "fully restored" and the function is set up we retrieve the elements we are
        # interested in. Since the nested_key_grabber - function is a generator we access its results with next()

        try:
            accommodation_name = next(nested_key_grabber("currentLocation", fully_restored_json))[0]["name"]
        except Exception as e:
            print(f"Error! {e} (accommodation_name)")
            accommodation_name = "N/A"

        accommodation_url = next(nested_key_grabber("initialAbsoluteUrl", access_json))
        accommodation_type = next(nested_key_grabber("accommodationType", fully_restored_json))

        ### Location
        try:
            location_latitude = next(nested_key_grabber("currentLocation", fully_restored_json))[0]["latitude"]
        except Exception as e:
            print(f"Error! {e} (location_latitude)")
            location_latitude = "N/A"

        try:
            location_longitude = next(nested_key_grabber("currentLocation", fully_restored_json))[0]["longitude"]
        except Exception as e:
            print(f"Error! {e} (location_longitude)")
            location_longitude = "N/A"

        try:
            location_coordinates = [location_latitude] + [location_longitude]
        except Exception as e:
            print(f"Error! {e} (location_coordinates)")
            location_coordinates = "N/A"

        try:
            location_address = next(nested_key_grabber("currentLocation", fully_restored_json))[0]["streetAddress"][
                "fullAddress"]
        except Exception as e:
            print(f"Error! {e} (location_address)")
            location_address = "N/A"

        try:
            location_id = next(nested_key_grabber("currentLocation", fully_restored_json))[0]["locationId"]
        except Exception as e:
            print(f"Error! {e} (location_id)")
            location_id = "N/A"

        try:
            tripadvisor_region_id = next(nested_key_grabber("parentGeoId", fully_restored_json))
        except Exception as e:
            print(f"Error! {e} (tripadvisor_region_id)")
            tripadvisor_region_id = "N/A"

        try:
            region_language = next(nested_key_grabber("currentLocation", fully_restored_json))[0]["localLanguage"]
        except Exception as e:
            print(f"Error! {e} (region_language)")
            region_language = "N/A"

        try:
            distance_unit = next(nested_key_grabber("nearbyWithPreferredPOIs", fully_restored_json))["distanceUnit"]
        except Exception as e:
            print(f"Error! {e} (distance_unit)")
            distance_unit = "N/A"

        #########
        try:
            nearby_transit = []
            for item in next(nested_key_grabber("nearbyTransit", fully_restored_json)):
                one_transit = {}
                one_transit.update({"locationDescription": next(nested_key_grabber("locationDescription", item))})
                one_transit.update({"name": next(nested_key_grabber("name", item))})
                one_transit.update(
                    {"linear_distance_to_location": next(nested_key_grabber("distanceFromCenter", item))})

                nearby_transit.append(one_transit)

        except Exception as e:
            print(f"Error! {e} (nearby_transit)")
            nearby_transit = "N/A"

        ####
        try:
            nearby_airport = []
            for item in next(nested_key_grabber("nearbyAirports", fully_restored_json)):
                one_airport = {}
                one_airport.update({"name": next(nested_key_grabber("locationName", item))})
                one_airport.update(
                    {"linear_distance_to_location": next(nested_key_grabber("distanceFromCenter", item))})
                nearby_airport.append(one_airport)
        except Exception as e:
            print(f"Error! {e} (nearby_airport)")
            nearby_airport = "N/A"

        ####
        try:
            distance_range = next(nested_key_grabber("nearbyWithPreferredPOIs", fully_restored_json))["distanceRange"]
        except Exception as e:
            print(f"Error! {e} (distance_range)")
            distance_range = "N/A"

        try:
            attraction_count = next(nested_key_grabber("nearbyWithPreferredPOIs", fully_restored_json))[
                "attractionCount"]
        except Exception as e:
            print(f"Error! {e} (attraction_count)")
            attraction_count = "N/A"

        try:
            hotel_count = next(nested_key_grabber("nearbyWithPreferredPOIs", fully_restored_json))["hotelCount"]
        except Exception as e:
            print(f"Error! {e} (hotel_count)")
            hotel_count = "N/A"

        try:
            restaurant_count = next(nested_key_grabber("nearbyWithPreferredPOIs", fully_restored_json))[
                "restaurantCount"]
        except Exception as e:
            print(f"Error! {e} (restaurant_count)")
            restaurant_count = "N/A"

        try:
            nearby_attractions_summary = {}
            nearby_attractions_summary.update({"distance_range": distance_range,
                                               "attraction_count": attraction_count,
                                               "hotel_count": hotel_count,
                                               "restaurant_count": restaurant_count
                                               })
        except Exception as e:
            print(f"Error! {e} (nearby_attractions_summary)")
            nearby_attractions_summary = "N/A"

        ####
        try:
            walkScore_TA = next(nested_key_grabber("walkScore", fully_restored_json))
        except Exception as e:
            print(f"Error! {e} (walkScore_TA)")
            walkScore_TA = "N/A"

        ###
        try:
            nearby_locations_detail = []
            for item in next(nested_key_grabber("nearbyLocationList", fully_restored_json)):
                one_location = {}
                one_location.update({"location_type": next(nested_key_grabber("placeType", item))})

                one_location.update({"location_name": next(nested_key_grabber("name", item))})
                one_location.update({"location_linear_distance": next(nested_key_grabber("distanceFromCenter", item))})

                location_latitude = next(nested_key_grabber("latitude", fully_restored_json))
                location_longitude = next(nested_key_grabber("longitude", fully_restored_json))
                location_coordinates = [location_latitude] + [location_longitude]

                one_location.update({"location_coordinates": location_coordinates})
                one_location.update({"location_name": next(nested_key_grabber("name", item))})
                one_location.update({"location_rating": next(nested_key_grabber("rating", item))})
                one_location.update({"location_rating_count": next(nested_key_grabber("count", item))})

                try:
                    attraction_tags = []
                    for attraction in next(nested_key_grabber("detail", item))["type"]:
                        attraction_tags.append(attraction["tagNameLocalized"])
                    one_location.update({"location_detail": attraction_tags})

                except:
                    pass

                try:
                    eatery_tags = []
                    for attraction in next(nested_key_grabber("detail", item))["cuisines"]:
                        eatery_tags.append(attraction["tagNameLocalized"])
                    one_location.update({"location_detail": eatery_tags})
                except:
                    pass
                nearby_locations_detail.append(one_location)

        except Exception as e:
            print(f"Error! {e} (nearby_locations_detail)")
            nearby_locations_detail = "N/A"

        ###### Language
        try:
            accommodation_languages = []
            for language in next(nested_key_grabber("languagesSpoken", fully_restored_json)):
                accommodation_languages.append(language["amenityNameLocalized"])
        except Exception as e:
            print(f"Error! {e} (accommodation_languages)")
            accommodation_languages = "N/A"

        #### Hotel Class

        try:
            accommodation_stars = next(nested_key_grabber("starRating", fully_restored_json))[0]["tagNameLocalized"]

        except Exception as e:
            print(f"Error! {e} (accommodation_stars)")
            accommodation_stars = "N/A"

        try:
            star_rating_provider = next(nested_key_grabber("providerStarRatingSource", fully_restored_json))[0][
                "tooltipText"]
        except Exception as e:
            print(f"Error! {e} (star_rating_provider)")
            star_rating_provider = "N/A"

        ##### Ratings
        try:
            overall_rating = next(nested_key_grabber("rating", fully_restored_json))
        except Exception as e:
            print(f"Error! {e} (overall_rating)")
            overall_rating = "N/A"
        try:
            overall_rating_count = next(nested_key_grabber("reviewSummary", fully_restored_json))["count"]
        except Exception as e:
            print(f"Error! {e} (overall_rating)")
            overall_rating_count = "N/A"

        try:
            subratings = {}
            for subrating in next(nested_key_grabber("reviewSubratingAvgs", fully_restored_json)):

                if subrating["questionId"] == 10:
                    subratings.update({"overall_satisfaction_subrating": subrating["avgRating"]})

                if subrating["questionId"] == 11:
                    subratings.update({"rooms_subrating": subrating["avgRating"]})

                if subrating["questionId"] == 12:
                    subratings.update({"service_subrating": subrating["avgRating"]})

                if subrating["questionId"] == 13:
                    subratings.update({"value_subrating": subrating["avgRating"]})

                if subrating["questionId"] == 14:
                    subratings.update({"cleanliness_subrating": subrating["avgRating"]})

                if subrating["questionId"] == 47:
                    subratings.update({"location_subrating": subrating["avgRating"]})

                if subrating["questionId"] == 190:
                    subratings.update({"sleep_quality_subrating": subrating["avgRating"]})
        except Exception as e:
            print(f"Error! {e} (subratings)")
            subratings = "N/A"

        #### Amenities
        try:
            property_amenities_highlighted = []
            for feature in next(nested_key_grabber("highlightedAmenities", fully_restored_json))["propertyAmenities"]:
                property_amenities_highlighted.append(feature["amenityNameLocalized"])

            property_amenities_non_highlighted = []
            for feature in next(nested_key_grabber("nonHighlightedAmenities", fully_restored_json))[
                "propertyAmenities"]:
                property_amenities_non_highlighted.append(feature["amenityNameLocalized"])

            property_amenities = property_amenities_highlighted + property_amenities_non_highlighted

        except Exception as e:
            print(f"Error! {e} (property_amenities)")
            property_amenities = "N/A"

        try:
            room_features_highlighted = []
            for feature in next(nested_key_grabber("highlightedAmenities", fully_restored_json))["roomFeatures"]:
                room_features_highlighted.append(feature["amenityNameLocalized"])

            room_features_non_highlighted = []
            for feature in next(nested_key_grabber("nonHighlightedAmenities", fully_restored_json))["roomFeatures"]:
                room_features_non_highlighted.append(feature["amenityNameLocalized"])

            room_features = room_features_highlighted + room_features_non_highlighted

        except Exception as e:
            print(f"Error! {e} (room_features)")
            room_features = "N/A"

        try:
            room_types_highlighted = []
            for feature in next(nested_key_grabber("highlightedAmenities", fully_restored_json))["roomTypes"]:
                room_types_highlighted.append(feature["amenityNameLocalized"])

            room_types_non_highlighted = []
            for feature in next(nested_key_grabber("nonHighlightedAmenities", fully_restored_json))["roomTypes"]:
                room_types_non_highlighted.append(feature["amenityNameLocalized"])

            room_types = room_types_highlighted + room_types_non_highlighted

        except Exception as e:
            print(f"Error! {e} (room_types)")
            room_types = "N/A"

        ########### Special badges
        try:
            green_leaders_level = next(nested_key_grabber("greenLeader", fully_restored_json))
        except Exception as e:
            print(f"Error! {e} (green_leaders_level)")
            green_leaders_level = "N/A"

        try:
            travelers_choice_award = response.css(".eHWKb").css("img::attr(alt)").extract()
            print(type(travelers_choice_award))
        except Exception as e:
            print(f"Error! {e} (travelers_choice_award)")
            travelers_choice_award = "N/A"


        ##### Prices
        try:
            currency_used = next(nested_key_grabber("currency", access_json))
        except Exception as e:
            print(f"Error! {e} (currency_used)")
            currency_used = "N/A"



        main_offers = []
        for offer in next(nested_key_grabber("chevronOffers", access_json)):
            one_offer = {}

            try:
                one_offer.update({"provider_name": offer["data"]["dataAtts"]["data-vendorName"]})
            except KeyError:
                one_offer.update({"provider_name": "N/A"})

            try:
                one_offer.update({"price": offer["data"]["dataAtts"]["data-perNight"]})
            except KeyError:
                one_offer.update({"price": "N/A"})

            try:
                one_offer.update({"taxes": offer["data"]["dataAtts"]["data-taxesValue"]})
            except KeyError:
                one_offer.update({"taxes": "N/A"})

            main_offers.append(one_offer)



        textlink_offers = []
        for offer in next(nested_key_grabber("textLinkOffers", access_json)):
            one_offer = {}

            try:
                one_offer.update({"provider_name": offer["data"]["dataAtts"]["data-vendorName"]})
            except KeyError:
                one_offer.update({"provider_name": "N/A"})

            try:
                one_offer.update({"price": offer["data"]["dataAtts"]["data-perNight"]})
            except KeyError:
                one_offer.update({"price": "N/A"})

            try:
                one_offer.update({"taxes": offer["data"]["dataAtts"]["data-taxesValue"]})
            except KeyError:
                one_offer.update({"taxes": "N/A"})

            textlink_offers.append(one_offer)



        hidden_offers = []
        for offer in next(nested_key_grabber("hiddenOffers", access_json)):
            one_offer = {}

            try:
                one_offer.update({"provider_name": offer["data"]["dataAtts"]["data-vendorName"]})
            except KeyError:
                one_offer.update({"provider_name": "N/A"})

            hidden_offers.append(one_offer)


        try:
            price_percentiles_USD_cent = []
            for item in next(nested_key_grabber("percentiles", access_json)):
                one_item = {}
                one_item.update({"percentile_type": item["percentileType"]})
                one_item.update({"start_date": item["startDate"]})
                one_item.update({"end_date": item["endDate"]})
                one_item.update({"end_date": item["endDate"]})
                one_item.update({"range_high": item["pricesUSD"]["rangeHigh"]})
                one_item.update({"range_low": item["pricesUSD"]["rangeLow"]})
                one_item.update({"min_price": item["pricesUSD"]["min"]})
                one_item.update({"low_price": item["pricesUSD"]["low"]})
                price_percentiles_USD_cent.append(one_item)
        except Exception as e:
            print(f"Error! {e} (price_percentiles_USD_cent)")
            price_percentiles_USD_cent = "N/A"

        try:
            price_USD_cent_future = []
            for x in next(nested_key_grabber("items", access_json)):
                listitem = {}
                listitem.update({"date": x["date"]})
                listitem.update({"price_USD_cent": x["priceUSD"]})
                price_USD_cent_future.append(listitem)
        except Exception as e:
            print(f"Error! {e} (price_USD_cent_future)")
            price_USD_cent_future = "N/A"



        #### Photos
        try:
            front_photos = []
            for item in next(nested_key_grabber("windowPanes", fully_restored_json))[0]["albums"][0]["mediaList"]:
                front_photos.append(next(nested_key_grabber("photoSizes", item))[-1]["url"])
        except Exception as e:
            print(f"Error! {e} (front_photos)")
            front_photos = "N/A"


        #########################
        # In the last step we assign the extracted data to scrapy item-vessels which are defined in the items.py file

        items = TaAccommodationinfoItem()

        items["accommodation_name"] = accommodation_name
        items["accommodation_url"] = accommodation_url
        items["accommodation_type"] = accommodation_type
        items["location_coordinates"] = location_coordinates
        items["location_address"] = location_address
        items["location_id"] = location_id
        items["region_id"] = tripadvisor_region_id
        items["region_language"] = region_language
        items["distance_unit"] = distance_unit
        items["nearby_transit"] = nearby_transit
        items["nearby_airport"] = nearby_airport
        items["nearby_attractions_summary"] = nearby_attractions_summary
        items["walkScore_TA"] = walkScore_TA
        items["nearby_locations_detail"] = nearby_locations_detail
        items["accommodation_languages"] = accommodation_languages
        items["accommodation_stars"] = accommodation_stars
        items["star_rating_provider"] = star_rating_provider
        items["overall_rating"] = overall_rating
        items["overall_rating_count"] = overall_rating_count
        items["subratings"] = subratings
        items["property_amenities"] = property_amenities
        items["room_features"] = room_features
        items["room_types"] = room_types
        items["green_leaders_level"] = green_leaders_level
        items["travelers_choice_award"] = travelers_choice_award
        items["front_photos"] = front_photos

        items["currency_used"] = currency_used
        items["main_offers"] = main_offers
        items["textlink_offers"] = textlink_offers
        items["hidden_offers"] = hidden_offers
        items["price_percentiles_USD_cent"] = price_percentiles_USD_cent
        items["price_USD_cent_future"] = price_USD_cent_future

        yield items
#########################

