import os
import json
import unittest
from unittest.mock import patch, MagicMock
from EarthPicture.credentials_handler import CredentialsHandler
from EarthPicture.copernicus_connector import CopernicusConnector


class TestCredentialsHandler(unittest.TestCase):

    def setUp(self):
        """ Set up a temporary config file for testing. """
        self.config_file = 'test_credentials_config.json'
        self.handler = CredentialsHandler(config_file=self.config_file)

    def tearDown(self):
        """ Clean up the config file after each test. """
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_set_and_get_credentials(self):
        """ Test setting and retrieving credentials for a provider. """
        credentials = {"username": "test_user", "password": "test_pass"}
        self.handler.set_credentials("Copernicus", credentials)
        retrieved_credentials = self.handler.get_credentials("Copernicus")
        self.assertEqual(retrieved_credentials, credentials)

    def test_missing_credentials(self):
        """ Test retrieving credentials for a non-existent provider. """
        with self.assertRaises(ValueError):
            self.handler.get_credentials("NonExistentProvider")

    def test_malformed_config(self):
        """ Test handling of a malformed configuration file. """
        with open(self.config_file, 'w') as f:
            f.write("malformed content")  # Write invalid JSON
        with self.assertRaises(ValueError):
            self.handler.get_credentials("Copernicus")


class TestCopernicusConnector(unittest.TestCase):

    # Patch the SentinelAPI in the context of EarthPicture.copernicus_connector
    @patch('EarthPicture.copernicus_connector.SentinelAPI')
    def setUp(self, MockSentinelAPI):
        """ Set up a CopernicusConnector with mocked SentinelAPI. """
        # Create mock credentials in a test config file
        self.config_file = 'test_credentials_config.json'
        credentials = {"username": "test_user", "password": "test_pass"}
        self.handler = CredentialsHandler(config_file=self.config_file)
        self.handler.set_credentials("Copernicus", credentials)

        # Instantiate the CopernicusConnector with mocked SentinelAPI and test config file
        self.connector = CopernicusConnector(config_file=self.config_file)

        # Mock the API instance within CopernicusConnector
        self.mock_api = MockSentinelAPI.return_value

    def tearDown(self):
        """ Clean up the config file after each test. """
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_list_missions(self):
        """ Test the list_missions method. """
        # Mock a response with a set of platform names
        self.mock_api.query.return_value = {
            "1": {"platformname": "Sentinel-1"},
            "2": {"platformname": "Sentinel-2"},
            "3": {"platformname": "Sentinel-3"}
        }
        missions = self.connector.list_missions()
        self.assertIn("Sentinel-1", missions)
        self.assertIn("Sentinel-2", missions)
        self.assertIn("Sentinel-3", missions)

    @patch('shapely.geometry.Polygon')
    def test_search_data_with_coords(self, MockPolygon):
        """ Test the search_data method using GPS coordinates. """
        # Mock the query response from the API
        self.mock_api.query.return_value = {
            "1": {
                "title": "Sentinel Image 1",
                "beginposition": "2023-01-01T00:00:00Z",
                "endposition": "2023-01-01T23:59:59Z",
                "cloudcoverpercentage": 20,
                "size": "500 MB",
                "uuid": "abc123"
            }
        }

        # Perform search using coordinates as a bounding box
        area_coords = [(-5.0, 40.0), (5.0, 50.0)]
        results = self.connector.search_data(
            mission="Sentinel-2",
            start_date="2023-01-01",
            end_date="2023-01-31",
            area_coords=area_coords,
            max_cloud_cover=30
        )

        # Check that results match the mocked response
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Sentinel Image 1")

    def test_connector_initialization_with_missing_credentials(self):
        """ Test initialization when credentials are missing. """
        os.remove('test_credentials_config.json')  # Simulate missing credentials
        with self.assertRaises(ValueError):
            CopernicusConnector()


if __name__ == "__main__":
    unittest.main()
