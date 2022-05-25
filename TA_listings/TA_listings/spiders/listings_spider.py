import scrapy
import sys

sys.path.insert(0, "C:/Users/mkind/PycharmProjects/TripAdvisor_scrapers_2022")

from Input_directory.Input_file import input_url
from ..items import TaListingsItem



class listings_spider(scrapy.Spider):
    name = "listings_spider"

    # We use the spider's name to initialize the scraping process later on

    # This function is called by the scraper at the start to yield the crawling seed.
    # The self-parameter in Python refers to the current individual object of the class. By using self we access
    # variables that belong to the class. The self parameter is the FIRST PARAMETER OF ANY METHOD (Function in class).

    def start_requests(self):

        yield scrapy.Request(url=input_url)

    # This function processes the downloaded content (response parameter). The parameter **kwargs allows for named
    # arguments to be accessed by response - but will not be needed here.
    def parse(self, response, **kwargs):

        # The spider sorts processed data into "items" - vessels. Items are logical groupings of extracted data
        # points. Without them the output would be unstructured in the form of Python dictionaries. The blueprint for
        # the vessels is in the items.py file which got imported above. Now we declare all items to take on the form
        # of the blueprint
        items = TaListingsItem()

        # In the following we declare which elements of the downloaded website content we want to extract and store
        # in the vessel items. Therefore we look into the website html code (chrome: right click page, chose "inspect").

        # On the website all listings follow the same pattern. We first identify these blocks of code that contain
        # one single TripAdvisor listing each. You can look on TripAdvisor: each "listing-box" contains the
        # identifier "listItem".

        # Tipp: to see what you would gather with certain code activate the scrapy shell in your terminal by entering:
        # "scrapy shell" followed by the TripAdvisor-url from above. Scrapy will download one page into your short-term
        # memory with which you can experiment and see how items would be extracted.

        all_single_listings = response.css("div.listItem")

        # all_single_listings contains now a list of code-blocks, which belong to different listings. We now loop over
        # each list entry and extract data which we attribute to different objects. Check with the scrapy shell whether
        # you do indeed extract what you intend to extract.

        # Although you see prices displayed they cannot be easily scraped. They are dynamically loaded into the website.
        # If you disable Javascript on chrome you won't see any prices. We could scrape the dynamic content with
        # scrapy splash but this comes with other problems (double counting) we'll scrape prices at a later stage.

        for entry in all_single_listings:
            accommodation_name = entry.css(".listing_title").css("a::text").extract()
            accommodation_link = entry.css(".listing_title").css("a::attr(href)").extract()
            accommodation_id = entry.css(".listing_title").css("a::attr(id)").extract()
            accommodation_type = entry.css(".mb10").css(".label::text").extract()

            # once extracted the information gets fed into the items vessel. However, before we clean the data:
            # We remove the backspace before the name
            # We add the root url
            # We delete "property_" before each id
            # Accomodation_type does not scrape "Hotel" as a type because it is the default on TripAdvisor.
            # We assign "Hotel" to all listings with empty accommodation_type.

            items["accommodation_name"] = [x.strip(" ") for x in accommodation_name][0]
            items["accommodation_link"] = "https://www.tripadvisor.com" + str(accommodation_link).split("'")[1]
            items["accommodation_id"] = str(accommodation_id).split("_")[1].split("'")[0]

            if len(accommodation_type) == 0:
                items["accommodation_type"] = "Hotel"
            else:
                items["accommodation_type"] = accommodation_type[0]

            # at the end of each loop we generate an output
            yield items

        # After the spider has left the loop it shall go to the next page. We build a pagination-instruction:
        # We define the "next page" to be a specific link on the page.
        # We command the spider to follow "next page" and to return to the parse function if a next page is present.

        next_page = response.css("a.next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
