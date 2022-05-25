from pymongo import MongoClient
import pandas as pd
from Input_directory.Input_file import input_database
import collections

client = MongoClient()
db = client[input_database]
collection_liste = db["Accommodations/Copenhagen_Zealand/2022-02-10_15:56:54"]
collection_experimental = db["Accommodations/Copenhagen_Zealand/2022-02-10_15:59:16"]

data_liste = pd.DataFrame(list(collection_liste.find()))
data_experimental = pd.DataFrame(list(collection_experimental.find()))

#print(data_liste.accommodation_name)
#print(data_experimental.accommodation_name)

liste_list = data_liste.accommodation_url.tolist()
experimental_list = data_experimental.accommodation_url.tolist()

print(len(liste_list))
print(len(set(liste_list)))

print("-----------------")
print("kurz :", len(experimental_list))
print("kurz", len(set(experimental_list)))
print("-----------------")
print([item for item, count in collections.Counter(liste_list).items() if count > 1])

list_difference = []
for item in liste_list:
    if item not in experimental_list:
        list_difference.append(item)
print("-----------------")
print(liste_list)
