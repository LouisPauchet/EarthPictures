from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from EarthPicture.credentials_handler import CredentialsHandler
from shapely.geometry import Polygon
from datetime import date

class CopernicusConnector:
    def __init__(self, config_file='credentials_config.json'):
        """
        Initializes the CopernicusConnector, which connects to the Copernicus Open Access Hub API.
        This connector retrieves credentials from the specified configuration file and uses them to
        initialize the SentinelAPI.

        Args:
            config_file (str): Path to the configuration file containing credentials. Defaults to 'credentials_config.json'.

        Raises:
            ValueError: If the credentials for 'Copernicus' are not found in the specified configuration file.
        """
        credentials_handler = CredentialsHandler(config_file=config_file)
        credentials = credentials_handler.get_credentials("Copernicus")

        if credentials is None:
            raise ValueError("Copernicus credentials not found. Please set them using the CredentialsHandler.")

        # Initialize the Sentinel API with retrieved credentials
        self.api = SentinelAPI(credentials["username"], credentials["password"], 'https://scihub.copernicus.eu/dhus')

    def list_missions(self):
        """
        Lists available Sentinel missions by querying the Copernicus Open Access Hub.
        This method queries a wide date range to retrieve distinct platform names, representing available missions.

        Returns:
            list: A list of available Sentinel missions (e.g., ['Sentinel-1', 'Sentinel-2']).
        """
        # Query a broad date range and look for unique platform names
        products = self.api.query(
            date=('2014-01-01', date.today().strftime('%Y-%m-%d')),
            area=None
        )
        # Extract unique platform names (missions) from query results
        missions = {product['platformname'] for product in products.values()}

        return list(missions)

    def search_data(self, mission, start_date, end_date, area_geojson=None, area_coords=None, max_cloud_cover=None):
        """
        Searches for Sentinel data based on mission type, date range, and optional filters like area and cloud cover.

        Args:
            mission (str): Sentinel mission name, such as 'Sentinel-1' or 'Sentinel-2'.
            start_date (str): Start date for the search, in the format 'YYYY-MM-DD'.
            end_date (str): End date for the search, in the format 'YYYY-MM-DD'.
            area_geojson (str, optional): Path to a GeoJSON file defining the area of interest.
            area_coords (list of tuple, optional): List of GPS coordinates defining a bounding box or polygon.
                - For a bounding box, provide two coordinates: [(lon_min, lat_min), (lon_max, lat_max)].
                - For a polygon, provide at least three coordinates: [(lon1, lat1), (lon2, lat2), (lon3, lat3), ...].
            max_cloud_cover (int, optional): Maximum allowed cloud cover percentage, used only with optical data (e.g., Sentinel-2).

        Returns:
            list: A list of dictionaries containing metadata for each available product, including fields such as:
                - 'title': Title of the product.
                - 'beginposition': Start of the data acquisition period.
                - 'endposition': End of the data acquisition period.
                - 'cloudcoverpercentage': Cloud cover percentage, if available.
                - 'size': File size of the product.
                - 'uuid': Unique identifier for the product.

        Raises:
            ValueError: If `area_coords` is provided but is not formatted as either a bounding box or polygon.
        """
        platform_name = mission
        footprint = None

        # Determine area footprint based on provided inputs
        if area_geojson:
            footprint = geojson_to_wkt(read_geojson(area_geojson))
        elif area_coords:
            if len(area_coords) == 2:  # Assume bounding box if 2 coordinates provided
                lon_min, lat_min = area_coords[0]
                lon_max, lat_max = area_coords[1]
                footprint = Polygon([(lon_min, lat_min), (lon_min, lat_max), (lon_max, lat_max), (lon_max, lat_min)]).wkt
            elif len(area_coords) >= 3:  # Assume polygon if more than 2 coordinates provided
                footprint = Polygon(area_coords).wkt
            else:
                raise ValueError(
                    "Invalid area_coords format. Provide either two coordinates for a bounding box or at least three for a polygon.")

        # Perform the search with optional filters
        products = self.api.query(
            area=footprint,
            date=(start_date, end_date),
            platformname=platform_name,
            cloudcoverpercentage=(0, max_cloud_cover) if max_cloud_cover is not None else None
        )

        # Format the results
        product_list = [
            {
                "title": product['title'],
                "beginposition": product['beginposition'],
                "endposition": product['endposition'],
                "cloudcoverpercentage": product.get('cloudcoverpercentage', 'N/A'),
                "size": product['size'],
                "uuid": product['uuid']
            }
            for product in products.values()
        ]

        return product_list
