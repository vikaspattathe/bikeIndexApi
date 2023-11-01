import requests
import json
import shutil
import logging
from datetime import datetime, timedelta
import csv
import base64
from gpt import GPT
from PIL import Image
from io import BytesIO
import os

class BikeIndex:
    def __init__(self) -> None:
        FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
        logging.basicConfig(filename='./logs/Logs.log',format=FORMAT, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.url = "https://bikeindex.org:443/api/v3/"
        self.gpt = GPT()
        self.manufacturers = self.manufacturer_details_from_csv()
        

    def search_by_location(self, location: str, distance: int=10, manufacturer: str='') -> list:
        results = []
        page = 1
        
        try:
            while True:
                url = "{}search?page={}&per_page=100&manufacturer={}&location={}&distance={}&stolenness=proximity".format(self.url, page, manufacturer, location, distance)
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

                search_result = json.loads(response.text)
                self.logger.debug("Recieved Page: %d from bikeIndex API", page)
                
                if "bikes" in search_result:
                    if not search_result["bikes"] or search_result["bikes"] == []:
                        break

                    for bike in search_result.get("bikes", []):
                        results.append(bike)
                    if len(search_result["bikes"]) < 99:
                        break
                    page += 1
                else:
                    break
        except requests.exceptions.RequestException as e:
            self.logger.error("Error while searching for bikes: %s", e)  
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error("Error decoding JSON response: %s", e)
        except Exception as e:
            self.logger.error("An unexpected error occured: %s", e)
        return results

    def search(self,location: str, distance: int=10, manufacturer: str='', duration:int=6) -> list:
        results = self.search_by_location(location, distance, manufacturer)
        results = self.filter_by_time(results, duration)
        results = self.format_data(results)
        return results

    def write_manufacturer_details(self, bikes: list) -> list:
        csv_updated = False
        for bike in bikes:
            bike["manufacturer_details"] = ''
            if "manufacturer_name" in bike and not self.field_is_empty(bike["manufacturer_name"]):
                manufacturer = str(bike["manufacturer_name"])
                if manufacturer in self.manufacturers:
                    bike["manufacturer_details"] = self.manufacturers[manufacturer]
                else:
                    try:
                        details = self.gpt.get_manufacturer_details(manufacturer=manufacturer)
                        bike["manufacturer_details"] = details
                        self.manufacturers[manufacturer] = details
                        csv_updated = True
                    except Exception as e:
                        self.logger.error("Error while getting manufacturer details: %s", e)

        if csv_updated:
            self.manufacturer_details_to_csv()
        return bikes

    def manufacturer_details_from_csv(self) -> dict:
        self.manufacturers = {}
        try:
            with open("manufacturers.csv", mode='r', newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    manufacturer_name = row["manufacturer name"]
                    manufacturer_details = row["manufacturer details"]
                    self.manufacturers[manufacturer_name] = manufacturer_details

        except FileNotFoundError:
            self.logger.error("Missing Manufacturers.csv file: %s", e)
            self.logger.info("Creating manufacturers.csv file")
            with open("manufacturers.csv", mode='w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ['manufacturer name', 'manufacturer details']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                pass

        except Exception as e:
            self.logger.error("Error while reading manufacturers CSV: %s", e)

        return self.manufacturers

    def manufacturer_details_to_csv(self) -> None:
        try:
            with open("manufacturers.csv", mode='w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ["manufacturer name", "manufacturer_details"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()

                for manufacturer_name, manufacturer_details in self.manufacturers.items():
                    writer.writerow({"manufacturer name": manufacturer_name, "manufacturer details": manufacturer_details})
        except (OSError, PermissionError, FileNotFoundError) as e:
            self.logger.error("Error while writing to CSV: %s", e)

    def image_to_base64(self, bikes: list) -> list:
        for bike in bikes:
            bike["image_base64"] = ''
            large_img_url = bike['large_img']

            if "large_img" in bike and not self.field_is_empty(bike['large_img']):
                large_img_url = bike['large_img']

                try:
                    if large_img_url.startswith("https://"):
                        response = requests.get(large_img_url, stream=True)
                        response.raise_for_status()

                        image_data = response.content
                        image_base64 = str(base64.b64encode(image_data).decode('utf-8'))
                        bike['image_base64'] = image_base64
                except requests.exceptions.RequestException as e:
                    self.logger.error("Error while fetching image for bike %s: %s", bike['id'], e)
                except Exception as e:
                    self.logger.error("An unexpected error occurred while processing images: %s", e)
        return bikes

    def get_ids(self, search_result: dict) -> list:
        ids = []
        for bike in search_result["bikes"]:
            ids.append(bike["id"])
        return ids

    def search_by_id(self, bike_id:int) ->list:
        bike=[]
        url = "{}bikes/{}".format(self.url, bike_id)
        try:
            response = requests.get(url)
            response.raise_for_status()
            search_result = json.loads(response.text)
            bike=[search_result["bike"]]
            bike=self.format_data(bike)
        except requests.exceptions.RequestException as e:
            self.logger.error("Error while fetching bike details: %s", e)
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error("Error decoding JSON response: %s", e)
        except Exception as e:
            self.logger.error("An unexpected error occurred while searching by ID: %s", e)
        return bike

    def filter_by_time(self, search_result: list, months_ago: int) -> list:
        try:
            search_date = datetime.now() - timedelta(days=months_ago * 30)
            filtered_records = []

            for bike in search_result:
                if not self.field_is_empty(bike['date_stolen']):
                    date_stolen = datetime.utcfromtimestamp(bike['date_stolen'])
                    if date_stolen >= search_date:
                        filtered_records.append(bike)
        except Exception as e:
            self.logger.error("An error occurred while filtering by time: %s", e)
        return filtered_records

    def format_date(self, search_result: list) -> list:
        bikes = search_result
        for bike in bikes:
            if "date_stolen" in bike and bike["date_stolen"] is not None:
                try:
                    timestamp = bike["date_stolen"]
                    date_stolen = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y")
                    bike["date_stolen"] = date_stolen
                except Exception as e:
                    self.logger.error("An error occurred while formatting dates: %s", e)
        return bikes

    def field_is_empty(self, field) -> bool:
        if field == '' or field is None:
            return True
        return False
    
    def format_data(self, search_result: list) -> list:
        search_result = self.format_date(search_result)
        search_result = self.write_manufacturer_details(search_result)
        search_result = self.image_to_base64(search_result)
        return search_result

    '''
    def write_to_csv(self, bikes: list):
        if bikes is not None:
            try:
                csv_file_name = "stolen_bikes.csv"
                print("Writing {} records to csv".format(len(bikes)))
                fieldnames = set()
                for bike in bikes:
                    fieldnames.update(bike.keys())

                with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    writer.writeheader()
                    for bike in bikes:
                        writer.writerow(bike)

                print(f"Data saved to {csv_file_name}")
            except (OSError, PermissionError, FileNotFoundError) as e:
                print(f"Error while writing to CSV: {e}")
        else:
            print("No bike data found.")

    
    def save_as_image(self, bikes: list) -> None:
        if not os.path.exists('images'):
            os.makedirs('images')

        for bike in bikes:
            if bike['image_base64'] != '':
                try:
                    imagedata = base64.b64decode(bike['image_base64'])
                    decoded_image = Image.open(BytesIO(imagedata))
                    image_filename = os.path.join('images', '{}.jpg'.format(bike['id']))
                    decoded_image.save(image_filename)
                except Exception as e:
                    print(f"Error {e} while decoding image in bike {bike['id']}")
    '''

