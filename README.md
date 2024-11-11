# EarthPicture

**EarthPicture** is a Python package designed to provide public and easy access to time series of satellite imagery, with a particular focus on supporting climate studies. This package enables users to effortlessly retrieve and visualize satellite imagery over selected areas and create time-lapse videos to observe environmental and climate-related changes over time.

## Goals

The main goal of EarthPicture is to:
- Simplify access to satellite imagery for climate research and monitoring.
- Enable users to easily generate time-lapse visuals from satellite images to observe changes over time in specific geographic areas.
- Offer a flexible and user-friendly interface for working with data from major satellite data providers, such as Copernicus (Sentinel), with plans to support additional providers in the future.

## Planned Features

- **Time Series Access**: Retrieve sequences of satellite imagery over a specified time period, useful for studying climate-related changes.
- **Time-lapse Creation**: Generate time-lapse videos from imagery data to visualize changes over time.
- **Easy Area Selection**: Select areas of interest using either bounding box coordinates or GeoJSON files.
- **Data Access**: Interface with the Copernicus Open Access Hub and Planet API to query and retrieve satellite data based on mission, date range, cloud cover, and location.
- **Sphinx Documentation**: Clear and comprehensive documentation for ease of use.

## Installation

Clone the repository and install the required packages with `pip`:

```bash
git clone https://github.com/yourusername/EarthPicture.git
cd EarthPicture
pip install -r requirements.txt
