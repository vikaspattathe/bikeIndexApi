# Bike Index API
This project provides a RESTful API for searching and filtering stolen bikes from the BikeIndex website. It allows users to query and retrieve information about stolen bikes based on location, manufacturer,duration and range.

# Features
Stolen Bike Search: Easily search for stolen bikes with the below parameters.
    
    Location: Search by location or using the user's IP location by default.

    Duration: Filter bikes based on the duration since they were reported stolen (default is 6 months).
    
    Distance: Refine results within a specified range (default is 10 kilometers).
    
    Manufacturer Name: Find stolen bikes from a specific manufacturer by providing the manufacturer's name.

Manufacturer Information: Additional manufacturer details are obtained from GPT (OpenAI's GPT-3 model) and added to the response as "manufacturer_details". This information is saved to the 'manufacturers.csv' file which acts as datastore. This data(manufacturer name and manufacturer details) is imported to the application as a dictionary(key:value pair). The application will only access this next time the same manufacturer comes up, eliminating an api call to GPT improving efficiency and response times. 

Image Retrieval: Images of the stolen bikes are fetched from the web and converted into base64 encoding. These base64-encoded images are then included in the API response as "image_base64." This feature allows users to view images of stolen bikes directly through the API.

# GETTING STARTED 
1. Clone this repository to your local machine:
2. Create and use a virtual environment:

    python -m venv {environment_name}
    source {environment_name}/bin/activate

2. Install all the necessary libraries

    pip install -r requirements.txt

3. Replace OPEN_AI_KEY in gpt.py with your own key.
4. Run the application
    
    python main.py

5. You can view and test api on your browser : http://127.0.0.1:5000/

# USAGE
## User endpoints:
GET  http://127.0.0.1:5000/bikeindex/search: 
Allows users to search for stolen bikes based on various parameters like location, duration, distance and manufacturer name.

Request:

    {
        'location':'Dublin',
        'duration:3,
        'manufacturer':''
        'distance':10
    }

Response:
    
    {
    "count": 1,
    "bikes": [
        {
        "date_stolen": "12-08-2023",
        "description": null,
        "frame_colors": [
            "Blue"
        ],
        "frame_model": "Dual sport 3",
        "id": 1574238,
        "is_stock_img": false,
        "large_img": "https://files.bikeindex.org/uploads/Pu/733951/large_IMG_7571.png",
        "location_found": null,
        "manufacturer_name": "Trek",
        "external_id": null,
        "registry_name": null,
        "registry_url": null,
        "serial": "WTU45C9802T",
        "status": "stolen",
        "stolen": true,
        "stolen_coordinates": [
            53.38,
            -6.42
        ],
        "stolen_location": "Clonsilla, D15 P2P2, IE",
        "thumb": "https://files.bikeindex.org/uploads/Pu/733951/small_IMG_7571.png",
        "title": "2022 Trek Dual sport 3",
        "url": "https://bikeindex.org/bikes/1574238",
        "year": 2022,
        "manufacturer_details": "Trek is a renowned bike manufacturer founded in 1976, known for its innovative designs and high-quality bicycles. With a strong commitment to sustainability and performance, Trek has become a leading brand in the cycling industry.",
        "image_base64":''
        },
        ]
    }

GET http://127.0.0.1:5000/bikeindex/id: Enables users to search for a specific stolen bike by providing its unique ID.

Request:

    {
        'id':1335559
    }

Response:
    
    {
        "date_stolen": "02-07-2023",
        "description": "Green front basket, stickers on frame, rear rack, selle italia leather saddle, phone mount on handlebars",
        "frame_colors": [
            "Black",
            "Brown"
        ],
        "frame_model": "Miss Grace",
        "id": 1335559,
        "is_stock_img": false,
        "large_img": "https://files.bikeindex.org/uploads/Pu/718026/large_gazelle-miss-grace-citybike-damen-schwarz-94909-b.jpg",
        "location_found": null,
        "manufacturer_name": "Gazelle",
        "external_id": null,
        "registry_name": null,
        "registry_url": null,
        "serial": "GZ12701667",
        "status": "stolen",
        "stolen": true,
        "stolen_coordinates": [
            53.34,
            -6.28
        ],
        "stolen_location": "Dublin, D08YT99, IE",
        "thumb": "https://files.bikeindex.org/uploads/Pu/718026/small_gazelle-miss-grace-citybike-damen-schwarz-94909-b.jpg",
        "title": "2022 Gazelle Miss Grace",
        "url": "https://bikeindex.org/bikes/1335559",
        "year": 2022,
        "registration_created_at": 1656680008,
        "registration_updated_at": 1688360969,
        "api_url": "https://bikeindex.org/api/v1/bikes/1335559",
        "manufacturer_id": 150,
        "paint_description": null,
        "name": "Miss Grace",
        "frame_size": "49cm",
        "rear_tire_narrow": false,
        "front_tire_narrow": false,
        "type_of_cycle": "Bike",
        "test_bike": false,
        "rear_wheel_size_iso_bsd": 622,
        "front_wheel_size_iso_bsd": 622,
        "handlebar_type_slug": null,
        "frame_material_slug": "aluminum",
        "front_gear_type_slug": "1",
        "rear_gear_type_slug": "1-internal",
        "extra_registration_number": null,
        "additional_registration": null,
        "stolen_record": {
            "date_stolen": 1688252400,
            "location": "Dublin, D08YT99, IE",
            "latitude": 53.34,
            "longitude": -6.28,
            "theft_description": "Left the apartment for two hours and it was gone when we came back, it was locked outside the apartment",
            "locking_description": "Other",
            "lock_defeat_description": "Lock is missing, along with the bike",
            "police_report_number": "",
            "police_report_department": "",
            "created_at": 1688291433,
            "create_open311": false,
            "id": 146000
        },
        "public_images": [
            {
            "name": "2022 Gazelle Miss Grace Black and Brown",
            "full": "https://files.bikeindex.org/uploads/Pu/718026/gazelle-miss-grace-citybike-damen-schwarz-94909-b.jpg",
            "large": "https://files.bikeindex.org/uploads/Pu/718026/large_gazelle-miss-grace-citybike-damen-schwarz-94909-b.jpg",
            "medium": "https://files.bikeindex.org/uploads/Pu/718026/medium_gazelle-miss-grace-citybike-damen-schwarz-94909-b.jpg",
            "thumb": "https://files.bikeindex.org/uploads/Pu/718026/small_gazelle-miss-grace-citybike-damen-schwarz-94909-b.jpg",
            "id": 718026
            }
        ],
        "components": [],
        "manufacturer_details": "Gazelle is a renowned Dutch bike manufacturer that was founded in 1892. They are known for their high-quality bicycles that combine style, comfort, and durability.",
        "image_base64": '',
    }



