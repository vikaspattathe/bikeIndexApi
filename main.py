from bike_index import BikeIndex
import csv
from datetime import datetime


if __name__ == "__main__":
    # INSTANTIATE BikeIndex OBJECT
    bi = BikeIndex()
    location = "Dublin"
    distance = 15

    print("Searching for stolen bikes in {}...".format(location))
    search_result = bi.search_by_location(location)
    search_result=bi.format_date(search_result)
    print(search_result[0:3])


