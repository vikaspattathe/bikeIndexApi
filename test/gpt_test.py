import unittest
from unittest.mock import patch, Mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 
from gpt import GPT
import openai


class TestGPT(unittest.TestCase):

    def test_get_manufacturer_details_error(self):
        gpt = GPT()
        gpt.get_from_gpt = Mock(return_value="")
        
        details = gpt.get_manufacturer_details("TestManufacturer")
        
        self.assertEqual(details, "")

if __name__ == "__main__":
    unittest.main()
