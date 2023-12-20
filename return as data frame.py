import requests
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_columns', None)               # show all columns
pd.set_option('display.expand_frame_repr', False)        # do not wrap


class WebScraper:
    def __init__(self, keyword):
        self.keyword = keyword

    # define job categories and pages 
    def get_jobs(self):
        all_jobs_data = []
        page = 1
        while True:
            page_url = f"https://www.seek.co.nz/{self.keyword}-jobs/in-All-New-Zealand?sortmode=ListedDate&page={page}"
            page_data = self.scrape_page(page_url)
            if not page_data:
                break  
            all_jobs_data.extend(page_data)
            page += 1

        return all_jobs_data
    
    # define job scraping and pages 
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
        
    # define null value data 
    def get_text(self, parent, tag, attrs):
        element = parent.find(tag, attrs)
        return element.get_text(strip=True) if element else None

# retrive key job title
keywords = ["data-engineer", "BI-developer", "Data-Consultant"]
all_jobs_data = []

for keyword in keywords:
    scraper = WebScraper(keyword)
    jobs_data = scraper.get_jobs()
    all_jobs_data.extend(jobs_data)

# convert all data to Pandas DataFrame
df = pd.DataFrame(all_jobs_data)
print(df)

