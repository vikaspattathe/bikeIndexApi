# Bike Index API
This project provides a RESTful API for searching and filtering stolen bikes from the BikeIndex website. It allows users to query and retrieve information about stolen bikes based on location, manufacturer,duration and range.


# Features
Stolen Bike Search: Easily search for stolen bikes with the below parameters.
    Location: Search by location or using the user's IP location by default.
    Duration: Filter bikes based on the duration since they were reported stolen (default is 6 months).
    Distance: Refine results within a specified range (default is 10 kilometers).
    Manufacturer Name: Find stolen bikes from a specific manufacturer by providing the manufacturer's name.

Manufacturer Information: Additional manufacturer details are obtained from GPT (OpenAI's GPT-3 model) and added to the response as "manufacturer_details." This information is saved to the "manufacturers.csv" file to reduce API calls, improving efficiency and response times.

Image Retrieval: Images of the stolen bikes are fetched from the web and converted into base64 encoding. These base64-encoded images are then included in the API response as "image_base64." This feature allows users to view images of stolen bikes directly through the API.

Filter Records: Filter through stolen bikes using location, duration, distance and manufacturer name.

# DATA
{
    "id": 0,
    "manufacturer_name": "string",
    "manufacturer_details": "string",
    "date_stolen": "string",
    "image_base64": "string",
    "description": "string",
    "frame_colors": ["string"],
    "frame_model": "string",
    "is_stock_img": true,
    "large_img": "string",
    "location_found": "string",
    "external_id": 0,
    "registry_name": "string",
    "registry_url": "string",
    "serial": "string",
    "status": "string",
    "stolen": true,
    "stolen_coordinates": [int],
    "stolen_location": "string",
    "thumb": "string",
    "title": "string",
    "url": "string",
    "year": 0,
    "propulsion_type_slug": "string",
    "cycle_type_slug": "string"
}

# USAGE
The Bike Index API provides two main endpoints:

bikeindex/search: Allows users to search for stolen bikes based on various parameters like location, duration, distance and manufacturer name.

bikeindex/id: Enables users to search for a specific stolen bike by providing its unique ID.

# GETTING STARTED 
1. Clone this repository to your local machine:
2. Install all the necessary libraries - 'pip install -r requirements.txt'
3. Replace OPEN_AI_KEY in gpt.py with your own key.
4. Run the application - 'python main.py'

