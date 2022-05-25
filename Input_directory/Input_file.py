from pymongo import MongoClient


#### Input General
input_database = "Masterthesis_Database"

############# Input Accommodation_spider
input_url = "https://www.tripadvisor.de/Hotels-g227880-Gummersbach_North_Rhine_Westphalia-Hotels.html"

############# Input Reviews_spider

select_accommodation_TYPE = "T_HOTEL"

""" Available types

T_HOTEL                       
T_LIMITED_SERVICE_PROPERTY    
T_BEDANDBREAKFAST             
T_HOSTEL                      
T_GUEST_HOUSE                 
T_CONDO                       
T_SPECIAL_HOTEL                
T_VILLA                        
T_LODGE                        
T_APARTMENT_HOTEL              
T_INN                          
T_SMALL_HOTEL                  
T_SPECIAL_INN                  
T_CAMPGROUND                   
T_SPECIAL_RESORT               
T_MOTEL                        
T_SPECIAL_BNB                  

"""

##################################### MongoDB setup #########################################

# With every run the listings_spider creates a new MongoDB collection with the following name format:
# "type/location/time". These names are useful since MongoDB collections do not feature any metadata - so the metadata
# is in the name.

# To make the metadata useful we create a list of all collections in the database. Then we split up the names in their
# metadata components:
#                       ["type/location/time","type/location/time"...] -> ["type","location","time","type"...]

client = MongoClient()
db = (client[input_database].list_collection_names())
db_split = [i.split("/") for i in db]

# Now the metadata gets reassambled again into a list of dictionaries. I also glue the names together again and assign
# them the key "name":
#                      ["type","location","time","type"...] ->
#                      [{"type" : "type", "location":"location", "time":"time", "name":"type/location/time"},{..}...]

keys = ["type",  "location", "time"]
db_collection_metadata = []
for i in db_split:
    liste = list(zip(keys, i))
    dictionary = dict(liste)
    add_name = {"name": "/".join(i)}
    dictionary.update(add_name)
    db_collection_metadata.append(dictionary)

# Now that we have the metadata attributed to separate keys we can FILTER the collection list for certain locations and
# we can SORT the filtered list by their time of creation. So that the newest collection will be on first position [0].

######################################################################################################################## Make Location dynamic! ( from input_url ??? )


def filter_sort(location):
    types_filter = [collection for collection in db_collection_metadata if collection["type"] == "Accommodations"]
    location_filter = [collection for collection in types_filter if collection["location"] == location]
    return sorted(location_filter, key=lambda i: i["time"], reverse=True)[0]["name"]


def filter_sort2():
    types_filter = [collection for collection in db_collection_metadata if collection["type"] == "Reviews"]
    return sorted(types_filter, key=lambda i: i["time"], reverse=True)[0]["name"]



reviews_filter = filter_sort("Copenhagen_Zealand")


########## Profile_spider (no Input)
profile_filter = filter_sort2()


