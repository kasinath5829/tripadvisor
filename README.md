# Trip Advisor Data Acquisition Project
# Overview
This repository contains the code and documentation for a data acquisition project focused on scraping hotel information from TripAdvisor and other major Online Travel Agencies (OTAs). The project aims to gather comprehensive data for analysis and business intelligence within the hospitality industry.

# Project Structure
Code: Contains Python scripts for web scraping, data extraction, and MongoDB database management.

Data: Includes extracted data in JSON format and HTML files containing scraped TripAdvisor search result pages.

Prerequisites
Python 3.x
Libraries: requests, BeautifulSoup, pymongo
Usage
Scraping TripAdvisor:

Run Initial_code.py to download TripAdvisor search result pages as HTML files.
Database Connection:

Execute Run_this_second.py to establish a connection to MongoDB and create a database for storing scraped data.
Scraping OTA Information:

Run Run_this_last.py to update the database with hotel pricing data from major OTAs.
Directory Structure
Code/
Initial_code.py
Run_this_second.py
Run_this_last.py
Data/
trip_advisor_search_pg1.html
trip_advisor_search_pg2.html
extracted_data.json
Usage Notes
Ensure internet connectivity while running scripts to access web data.
Adjust parameters (e.g., dates, search criteria) within scripts for customization.
Contributing
Contributions and suggestions are welcome! Fork the repository, make changes, and submit a pull request.

