from pymongo import MongoClient
import pandas as pd
from Input_directory.Input_file import input_database,reviews_filter, select_accommodation_TYPE,db_collection_metadata



client = MongoClient()
db = client[input_database]
collection = db[reviews_filter]
data = pd.DataFrame(list(collection.find()))

print(data)


print(data.accommodation_type.value_counts())

filter_for_accommodation_type = data.loc[data["accommodation_type"] == select_accommodation_TYPE]

for document in filter_for_accommodation_type.accommodation_url:
    print(document)


print(db_collection_metadata)

