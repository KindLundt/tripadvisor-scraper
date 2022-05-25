import json
import re

open_json = open("C:/Users/mkind/OneDrive/Desktop/Old_TripAdvisor_Json.txt", encoding="utf8")
read_json = open_json.read()
json_object = json.loads(read_json)


print(type(read_json))
print(json_object)


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



hotel_id = next(nested_key_grabber("currentLocation", json_object))[0]["locationId"]
hotel_name = next(nested_key_grabber("currentLocation", json_object))[0]["name"]

print(hotel_id)
print(hotel_name)