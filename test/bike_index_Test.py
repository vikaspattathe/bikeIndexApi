import unittest
from unittest.mock import patch, Mock, call, mock_open

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 
from bike_index import BikeIndex 

class TestBikeIndex(unittest.TestCase):
    def setUp(self):
        self.bike_index = BikeIndex()

    @patch('requests.get')
    def test_search_by_location_success(self, mock_get):
        #mock the successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"bikes": [{"id": 1}, {"id": 2}]}'
        mock_get.return_value = mock_response

        results = self.bike_index.search_by_location("New York", 10, "Trek")

        #ensuring the API was called with the correct URL
        expected_url = "https://bikeindex.org:443/api/v3/search?page=1&per_page=100&manufacturer=Trek&location=New York&distance=10&stolenness=proximity"
        mock_get.assert_called_once_with(expected_url)

        #ensuring the results are as expected
        self.assertEqual(results, [{"id": 1}, {"id": 2}])

    @patch('requests.get')
    def test_search_by_location_empty_result(self, mock_get):
        #mock an empty API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"bikes": []}'
        mock_get.return_value = mock_response

        results = self.bike_index.search_by_location("Los Angeles", 15)

        #ensuring the API was called with the correct URL
        expected_url = "https://bikeindex.org:443/api/v3/search?page=1&per_page=100&manufacturer=&location=Los Angeles&distance=15&stolenness=proximity"
        mock_get.assert_called_once_with(expected_url)

        #ensuring the results are empty
        self.assertEqual(results, [])

    @patch('requests.get')
    def test_search_by_location_error(self, mock_get):
        #mock an API error response
        mock_get.side_effect = Exception("API Error")

        results = self.bike_index.search_by_location("San Francisco", 5)

        #ensuring an empty list is returned on error
        self.assertEqual(results, [])

    @patch('requests.get')
    def test_search_by_location_multiple_pages(self, mock_get):
        #mock multiple pages of API responses
        mock_list = list(range(1, 101))

        mock_responses = [
            Mock(status_code=200, text=f'{{"bikes": {mock_list}}}'),
            Mock(status_code=200, text=f'{{"bikes": {mock_list}}}'),
            Mock(status_code=200, text='{"bikes": []}')]
        mock_get.side_effect = mock_responses

        results = self.bike_index.search_by_location("Chicago", 8)

        #ensuring the API was called for each page
        expected_urls = [
            "https://bikeindex.org:443/api/v3/search?page=1&per_page=100&manufacturer=&location=Chicago&distance=8&stolenness=proximity",
            "https://bikeindex.org:443/api/v3/search?page=2&per_page=100&manufacturer=&location=Chicago&distance=8&stolenness=proximity",
            "https://bikeindex.org:443/api/v3/search?page=3&per_page=100&manufacturer=&location=Chicago&distance=8&stolenness=proximity"
        ]
        expected_calls = [call(url) for url in expected_urls]
        mock_get.assert_has_calls(expected_calls)

        #ensuring all results are collected
        self.assertEqual(results, mock_list*2)

    @patch('gpt.GPT')
    def test_write_manufacturer_details_missing_manufacturer_name(self, mock_gpt):
        #manufacturer name is empty
        bike = {"manufacturer_name": ""}
        bike_index = BikeIndex()
        result = bike_index.write_manufacturer_details([bike])
        self.assertEqual(result[0]['manufacturer_details'], '')
        self.assertFalse(mock_gpt.get_manufacturer_details.called)
    
    @patch('gpt.GPT')    
    def test_write_manufacturer_details_existing_manufacturer(self, mock_gpt):
        #manufacturer name exists in manufacturers
        existing_manufacturer = "Existing Manufacturer"
        bike = {"manufacturer_name": existing_manufacturer}
        bike_index = BikeIndex()
        bike_index.manufacturers[existing_manufacturer] = "Manufacturer Details"
        self.assertFalse(mock_gpt.get_manufacturer_details.called)   

    @patch('gpt.GPT')
    def test_write_manufacturer_details_gpt_error(self, mock_gpt):
        # Manufacturer name not in manufacturers, GPT call raises an exception
        bike = {"manufacturer_name": "New Manufacturer"}
        bike_index = BikeIndex()
        mock_gpt_instance = mock_gpt.return_value
        mock_gpt_instance.get_manufacturer_details.side_effect = Exception("GPT Error")
        result = bike_index.write_manufacturer_details([bike])
        expected_result = [{"manufacturer_name": "New Manufacturer", "manufacturer_details": ""}]
        self.assertEqual(result, expected_result)

    def test_filter_by_time(self):
        #test the filter_by_time method
        search_result = [
            {"id": 1, "date_stolen": 1635561600},  # Date: 30-10-2021
            {"id": 2, "date_stolen": 1667232000},  # Date: 30-10-2022
        ]
        bikeIndex=BikeIndex()
        months_ago = 13  # 13 months
        filtered_records = bikeIndex.filter_by_time(search_result, months_ago)
        self.assertEqual(len(filtered_records), 1)

    def test_filter_by_time_no_records(self):
        #test the filter_by_time method when records out of duration
        search_result = [
            {"id": 1, "date_stolen": 1635561600},  # Date: 30-10-2021
            {"id": 2, "date_stolen": 1667232000},  # Date: 30-10-2022
        ]
        bikeIndex=BikeIndex()
        months_ago = 4  # 4 months
        filtered_records = bikeIndex.filter_by_time(search_result, months_ago)
        self.assertEqual(len(filtered_records), 0)

    def test_format_date_success(self):
        #test the format_date method
        search_result = [{"id": 1, "date_stolen": 1635561600}]  # Date: 30-10-2021
        bikeIndex=BikeIndex()
        formatted_result = bikeIndex.format_date(search_result)
        self.assertEqual(formatted_result[0]["date_stolen"], "30-10-2021")

    def test_field_is_empty(self):
        #test the field_is_empty method
        empty_field = ""
        non_empty_field = "Not empty"
        bikeIndex=BikeIndex()
        self.assertTrue(bikeIndex.field_is_empty(empty_field))
        self.assertFalse(bikeIndex.field_is_empty(non_empty_field))

if __name__ == '__main__':
    unittest.main()
