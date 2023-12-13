from time import sleep

import requests
from bs4 import BeautifulSoup
from app import toaster
import webbrowser


class WebScraper:
    def __init__(self):
        self.previous_listing_id = None

    def run(self):
        print('Webscraper Started')
        while True:
            print('Checking for new jobs')
            self.getSite()
            print('cockl and balls')
            sleep(60 * 1)   # 5 mins

    def getSite(self):
        r = requests.get(
            'https://www.seek.co.nz/software-developer-jobs/in-Wellington-Central-Wellington?sortmode=ListedDate'
        )
        soup = BeautifulSoup(r.content, features="html.parser")
        for listing in soup.find_all('article'):
            if listing.get('data-automation') == 'normalJob':
                if listing.get('data-job-id') != self.previous_listing_id:
                    print('Job Found. ID: ', listing.get('data-job-id'))
                    self.previous_listing_id = listing.get('data-job-id')
                    job_name = listing.get('aria-label')

                    temp = listing.find_all('span')
                    job_employer = temp[7].span.a.string

                    job_link = 'http://seek.co.nz' + temp[0].div.get('href')

                    winToastDisplay(job_name, job_employer, job_link)
                    break
                else:
                    break


def winToastDisplay(job_name, job_employer, job_link):
    toaster.show_toast(job_name, job_employer, callback_on_click=lambda: open_link(job_link), threaded=True)

def open_link(job_link):
    webbrowser.open(job_link, new=2)