import json
import re

open_txt = open("C:/Users/mkind/OneDrive/Desktop/Json_Hotel_test_fullpage.txt", encoding="utf8")
read_txt = open_txt.read()
data = re.search(r'window\.__WEB_CONTEXT__=(.*?});', read_txt).group(1)
data = data.replace('pageManifest', '"pageManifest"')
data = json.loads(data)


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


filters_a = re.search(r'\{\\\"travelersChoice(.*?})]}}"},', access_json).group(0)
filters_a_cleaned = filters_a.replace("\\\\n"," ")\
    .replace("\\","")\
    .replace("null", '"null"')\
    .replace("false", '"false"')\
    .replace("true", '"true"').removesuffix('"},')

xxx = json.loads(filters_a_cleaned)

front_photos = []
for item in next(nested_key_grabber("windowPanes", xxx))[0]["albums"][0]["mediaList"]:
    front_photos.append(next(nested_key_grabber("photoSizes", item))[-1]["url"])

total_amount_photos = next(nested_key_grabber("windowPanes", xxx))[0]["albums"][0]["totalMediaCount"]

traveler_submitted_photo_top = []
for item in next(nested_key_grabber("windowPanes", xxx))[1]["albums"][0]["mediaList"]:
    traveler_submitted_photo_top.append(next(nested_key_grabber("photoSizes", item))[-1]["url"])

panorama_photo_top = []
for item in next(nested_key_grabber("windowPanes", xxx))[1]["albums"][1]["mediaList"]:
    panorama_photo_top.append(next(nested_key_grabber("photoSizes", item))[-1]["url"])

room_photo_top = []
for item in next(nested_key_grabber("windowPanes", xxx))[1]["albums"][2]["mediaList"]:
    room_photo_top.append(next(nested_key_grabber("photoSizes", item))[-1]["url"])



print(xxx)
print(type(xxx))
print("-------------------------------------")

print("front photos: ", front_photos)
print("total_amount_photos: ", total_amount_photos)
print("traveler_submitted_photo_top: ", traveler_submitted_photo_top)
print("panorama_photo_top: ", panorama_photo_top)
print("room_photo_top: ", room_photo_top)
