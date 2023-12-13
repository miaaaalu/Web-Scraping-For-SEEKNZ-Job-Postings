import requests
from bs4 import BeautifulSoup
import json

class WebScraper:
    def __init__(self, keyword):
        self.keyword = keyword

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

        return all_jobs_data  # Return the list of jobs directl

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

# Write the combined data to a single JSON file
filename = "job_listing_export.json"
with open(filename, 'w') as file:
    json.dump(all_data, file, indent=4)

print(f"All data export to {filename}")

# Optionally, print the data or store it in a variable for later use
# Print the data in a nicely formatted JSON style
formatted_json = json.dumps(all_data, indent=4)
print(formatted_json)