import requests                     # used to fetch HTML content 
from bs4 import BeautifulSoup       # used to parse HTML and XML documents
import json                         # used to work with JSON data

class WebScraper:
    def __init__(self, keyword, url_template):
        self.keyword = keyword
        self.url_template = url_template

    # fetching job pages in a loop 
    def get_jobs(self):
        all_jobs_data = []
        page = 1
        while True:
            page_url = self.url_template.format(keyword=self.keyword, page=page)
            page_data = self.scrape_page(page_url)
            if not page_data:
                break
            all_jobs_data.extend(page_data)
            page += 1
        return all_jobs_data
    
    # scraping job list in a single page
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

## read config file
with open('config.json', 'r') as file:
    config = json.load(file)

# Using keywords listing
keywords = config['keywords']
url_template = config['url_template']

all_data = {}

for keyword in keywords:
    scraper = WebScraper(keyword, url_template)
    all_data[keyword] = scraper.get_jobs()  

# export data to a single JSON file
filename = "job_listing_export.json"
with open(filename, 'w') as file:
    json.dump(all_data, file, indent=4)

print(f"All data export to {filename}")

# print the data
formatted_json = json.dumps(all_data, indent=4)
print(formatted_json)