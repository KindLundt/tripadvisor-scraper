import json

import re

url = "https://www.tripadvisor.com/Hotel_Review-g189541-d237647-Reviews-Hotel_Bethel_Somandshjem-Copenhagen_Zealand.html"

open_json = open("C:/Users/mkind/OneDrive/Desktop/Python Project/GUI/Json_Hotel_test.json")
read_json = json.load(open_json)

#open_txt = open("C:/Users/mkind/OneDrive/Desktop/Json_Hotel_test.txt")
open_txt = open("C:/Users/mkind/OneDrive/Desktop/Json_Hotel_test_fullpage.txt", encoding="utf8")
read_txt = open_txt.read()
#print(read_txt)
#print(type(read_txt))

data = re.search(r'window\.__WEB_CONTEXT__=(.*?});', read_txt).group(1)
data = data.replace('pageManifest', '"pageManifest"')
data = json.loads(data)


print("data   ", data)



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


#print("access   ", access)
#print(access_json)


filters_a = re.search(r'\{\\\"cachedFilters(.*?})]}"},', access_json).group(0)
filters_a_cleaned = filters_a.replace("\\\\n"," ")\
    .replace("\\","")\
    .replace("null", '"null"')\
    .replace("false", '"false"')\
    .replace("true", '"true"').removesuffix('"},')


print(filters_a)

print(type(filters_a_cleaned))
print(filters_a_cleaned)

xxx = json.loads(filters_a_cleaned)

Michael = next(nested_key_grabber("locations", xxx))[0]["name"]
Thomas = next(nested_key_grabber("userProfile", xxx))["displayName"]
Annemarie = next(nested_key_grabber("displayName", xxx))
Detlef = next(nested_key_grabber("cachedFilters", xxx))
managementtext = next(nested_key_grabber("mgmtResponse", xxx))["text"]

print(Michael)
print(Thomas)
print(Annemarie)
print(Detlef)
print(managementtext)