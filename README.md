## Overview 
- Developing Tools: Visual Studio 
- Language: Python 3.8 
- Use case: job search 
- Data collected: Job Location, Company, short description, description, Job title, etc.
- Job Site: seek.co.nz
- Description: develop a service or personal used for fun that allows you to read and collect Job Posts of any company, applying filters (company name, specific keywords). 
- sample result refer to [export as json](/job_listing_export.json)
- scraper return as json: refer to [listing by json](/return%20as%20json.py)
- scraper return as data frame: refer to [listing by dataframe](/return%20as%20data%20frame.py.py)
  
![Alt text](image.png)

## Imports and Dependencies
```py
import requests                 # used to fetch HTML content 
from bs4 import BeautifulSoup   # used to parse HTML and XML documents
import json                     # used to work with JSON data
import pandas as pd
```


## sample code 
```py
import requests
from bs4 import BeautifulSoup
import json

class WebScraper:
    def __init__(self, keyword):
        self.keyword = keyword

    # fetching job lists from all pages in a loop 
    def get_jobs(self):
        all_jobs_data = []
        page = 1
        while True:
            #page_url = f"https://www.seek.co.nz/{self.keyword}-jobs/in-All-New-Zealand?sortmode=ListedDate&page={page}"
            page_url = f"https://www.seek.co.nz/{self.keyword}-jobs/in-All-Auckland?sortmode=ListedDate&page={page}"
            page_data = self.scrape_page(page_url)
            if not page_data:
                break  
            all_jobs_data.extend(page_data)
            page += 1

        return all_jobs_data  

    # scraping job data in a single page, by using 'request' and phrasing by 'BeautifulSoup'
    def scrape_page(self, url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            jobs_data = []

            job_listings = soup.find_all('article', attrs={'data-card-type': 'JobCard'})
            for job in job_listings:
                link_element = job.find('a', {'data-automation': 'jobTitle'})
                job_link = 'https://www.seek.co.nz' + link_element['href'] if link_element else None

                job_data = {
                    'job_id': job.get('data-job-id', None),
                    'job_link': job_link,
                    'title': self.get_text(job, 'a', {'data-automation': 'jobTitle'}),
                    'salary': self.get_text(job, 'a', {'data-automation': 'jobSalary'}),
                    'company': self.get_text(job, 'a', {'data-automation': 'jobCompany'}),
                    'location': self.get_text(job, 'a', {'data-automation': 'jobLocation'}),
                    'short_description': self.get_text(job, 'span', {'data-automation': 'jobShortDescription'})
                }
                jobs_data.append(job_data)
            
            return jobs_data
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
        
    def get_text(self, parent, tag, attrs):
        element = parent.find(tag, attrs)
        return element.get_text(strip=True) if element else None

# Using keywords listing
keywords = ["data-engineer", "BI-developer", "data-consultant"]
all_data = {}

for keyword in keywords:
    scraper = WebScraper(keyword)
    all_data[keyword] = scraper.get_jobs()  # Assign returned data to the keyword

# DATA EXPORT
filename = "job_listing_export.json"                # (1) export data to a single JSON file
with open(filename, 'w') as file:
    json.dump(all_data, file, indent=4)

print(f"All data export to {filename}")

formatted_json = json.dumps(all_data, indent=4)     # (2) print the data
print(formatted_json)
```