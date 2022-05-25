import json
import re

#open_txt = open("C:/Users/mkind/OneDrive/Desktop/Json_Hotel_test_fullpage.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/OneDrive/Desktop/Hotel_Coellner_Hof_fullsite.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/OneDrive/Desktop/strange_TA_listing_fullpage.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/OneDrive/Desktop/Bondehuset_fullpage.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/OneDrive/Desktop/scandicFacloner_fullpage_4_februar.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/OneDrive/Desktop/scandicFalconer_fullpage4_februar_scrapy.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/Downloads/absalon fullpage.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/Downloads/userprofile_absalon.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/Downloads/hotelbethel fullpage.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/Downloads/hotelkong fullpage.txt", encoding="utf8")

#open_txt = open("C:/Users/mkind/Downloads/wakeup nach laden.txt", encoding="utf8")
#open_txt = open("C:/Users/mkind/Downloads/wakeup schnell.txt", encoding="utf8")

open_txt = open("C:/Users/mkind/Downloads/scrapyview bethel.txt", encoding="utf8")

#open_txt = open("C:/Users/mkind/Downloads/Coellner Hof Februar fulltext.txt", encoding="utf8")
read_txt = open_txt.read()

data = re.search(r'window\.__WEB_CONTEXT__=(.*?});', read_txt).group(1)
data = data.replace('pageManifest', '"pageManifest"')
data = json.loads(data)
print(json.dumps(data))


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


access = next(nested_key_grabber('urqlCache', data))
access_json = json.dumps(access)
access_json = json.loads(access_json)
access_json = json.dumps(access_json)


clean_access_json = access_json.replace("\\\\n", " ")\
    .replace('\\\\"', "'")\
    .replace("\\", "")\
    .replace(' "{', '{')\
    .replace('}"},', '}},')\
    .removesuffix('"}}')
clean_access_json_with_suffix = clean_access_json + "}}"


fully_restored_json = json.loads(clean_access_json_with_suffix)
xxx = json.dumps(fully_restored_json)
print(xxx)
print("---------------")
#############################################################################################
print(next(nested_key_grabber("chevronOffers", data)))
print("---------------")



main_offers = []
for offer in next(nested_key_grabber("chevronOffers", data)):
    one_offer = {}
    one_offer.update({"provider_name": offer["data"]["dataAtts"]["data-vendorName"]})
    one_offer.update({"price": offer["data"]["dataAtts"]["data-perNight"]})
    one_offer.update({"taxes": offer["data"]["dataAtts"]["data-taxesValue"]})
    main_offers.append(one_offer)
print(main_offers)
print("---------------------------------------------------")
print("---------------------------------------------------")
print(next(nested_key_grabber("textLinkOffers", data))[0]["data"]["dataAtts"]["data-vendorName"])

textlink_offers = []
for offer in next(nested_key_grabber("textLinkOffers", data)):
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

print(textlink_offers)

