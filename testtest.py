import re
import json
import requests

url = 'https://www.tripadvisor.com.ph/Hotel_Review-g8762949-d1085145-Reviews-El_Rio_y_Mar_Resort-San_Jose_Coron_Busuanga_Island_Palawan_Province_Mimaropa.html'
html_text = requests.get(url).text

data = re.search(r'window\.__WEB_CONTEXT__=(.*?});', html_text).group(1)
data = data.replace('pageManifest', '"pageManifest"')
data = json.loads(data)

# uncomment this to print all data:
# print(json.dumps(data, indent=4))

def traverse(val):
    if isinstance(val, dict):
        for k, v in val.items():
            if k == 'reviews':
                yield v
            else:
                yield from traverse(v)
    elif isinstance(val, list):
        for v in val:
            yield from traverse(v)

for reviews in traverse(data):
    for r in reviews:
        print(r['userProfile']['displayName'])
        print(r['title'])
        print(r['text'])
        print('Rating:', r['rating'])
        print('-' * 80)