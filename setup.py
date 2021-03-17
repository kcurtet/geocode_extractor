"""Setup.py - Package definition."""
from setuptools import setup

setup(
    name="geocode_extractor",
    version="0.0.1",
    description="Google Geocode API Extractor to csv",
    py_modules=["pandas", "geopy", "python-dotenv"],
    package_dir={'': 'src'}
)
