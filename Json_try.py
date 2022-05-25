from bs4 import BeautifulSoup
import requests
import json
import re

url = "https://www.tripadvisor.com/Hotel_Review-g189541-d237647-Reviews-Hotel_Bethel_Somandshjem-Copenhagen_Zealand.html"
url_wiki = "https://de.wikipedia.org/wiki/Otto_Braun"
header = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
"Dnt": "1",
"Host": "httpbin.org",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}


class TripHotelScraper:
    def __init__(self, url):
        self.url = url

        self.download_page()

        def download_page(self):

            # method for downloading the hotel page

            self.page = requests.get(self.url).text

         def scrape_data(self):

                #method for scraping out hotel name, address, and about

                soup = BeautifulSoup(self.page, "html.parser")

                hotel_name = soup.find("h1", {"id": "HEADING"}).text

                hotel_address = soup.find("span", {"class": "eWZDY _S eCdbd yYjkv"}).text

                hotel_about = soup.find("div", {"class": "pIRBV _T"}).text

                return {"name": hotel_name,

                        "about": hotel_about,

                        "address": hotel_address

                        }









source = requests.get(url, headers=header).text

soup = BeautifulSoup(source, 'lxml')

"""target_script = soup.find('script', text=re.compile('__WEB_CONTEXT__'))
json_data = re.search(r'({.*});', target_script.string).group(1)
json_data = json_data.replace('pageManifest', '"pageManifest"', 1)
data = json.loads(json_data)"""

print(soup)

"""

open_json = open("C:/Users/mkind/OneDrive/Desktop/Python Project/GUI/Json_Hotel_test.json")
read_json = json.load(open_json)
open_txt = open("C:/Users/mkind/OneDrive/Desktop/Json_Hotel_test.txt")
read_txt = open_txt.read()

with open("C:/Users/mkind/OneDrive/Desktop/Json_Hotel_test_fullpage.txt") as f2:
    datatext =f2.read()
    print(datatext)



datal = re.search(r'window\.__WEB_CONTEXT__=(.*?});', read_txt_fullpage).group(1)
data1 = datal.replace('pageManifest', '"pageManifest"')
data2 = json.loads(data1)

print(data)
print(data1)
print(data2)


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


for reviews in traverse(data2):
    for r in reviews:
        print("hello")

        print(r['userProfile']['displayName'])
        print(r['title'])
        print(r['text'])
        print('Rating:', r['rating'])
        print('-' * 80)

print(read_json)
print(read_txt)
print("--------------------------------------")
print(data)

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

resp = v.xpath("//script[contains(.,'requests')]/text()").extract_first()

"""