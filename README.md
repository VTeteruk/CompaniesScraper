# Renovation Leads Scraper
## Overview
This Python script is designed to scrape renovation _**(or other fields)**_ leads from Google Maps and gather information about business owners from the UK government website. The script utilizes Selenium for web scraping, Pandas for data manipulation, and tqdm for progress tracking.
___
## Features
* **Google Maps Scraper:** Generates a Google Maps URL based on the specified companies' field and city. It then extracts renovation leads' information from the Google Maps search results.

* **UK Government Website Scraper:** Searches for business owners associated with each renovation lead on the UK government website. It collects information such as the person's name, role, and status tag.

* **Data Processing and Saving:** The collected data is processed into a DataFrame using Pandas and saved to both CSV and Excel files.
___
## Requirements
1. [Python 3.x](https://www.python.org/downloads/) must be installed.
2. Create and activate your virtual environment:
   * For Mac/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * For Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate.bat
     ```
3. Install the required Python libraries using the following command:
   ```bash
   pip install -r requirements.txt
___
## Usage
Run the script using the following command:

```bash
python starter.py
```
Follow the on-screen prompts to enter the companies' field and city or use the default values.

The script will generate Google Maps URLs, scrape data, search for business owners, and save the results to CSV and Excel files.
___
## Settings
You can customize the script behavior by modifying the settings in the `settings.py` file.

Adjust parameters such as the default companies' field, default city, file paths for saving results, and more.

**NOTE:**

* `INPUT_MODE = False` - allows you to run the script with default values for companies' field and city without prompting user input. This is useful if you want to automate the script for a specific field and city without manual input.

* `HEADLESS = True` - allows you to hide the browser.
___
## Project Issues
* The `scroll_to_the_end_of_sidebar` method in [google_maps_parser.py](parsers/google_maps_parser.py) is intentionally designed to provide a safe and reliable way of navigating through the Google Maps sidebar (as sometimes Google Maps may just freeze). While there might be faster scrolling techniques, this method has proven to be robust and effective through extensive testing.


* The `extract_business_owners` method in [owners_parser.py](parsers/owners_parser.py) employs the use of the `person_index` parameter to accommodate scenarios where a company might have multiple owners or where other staff members are specified. This flexibility allows for a more comprehensive and accurate extraction of business ownership information.
