import requests
import selectorlib
import time
import sqlite3
from datetime import datetime, timezone
from database import create_tables
from database import add_new_job


URL = "https://www.jobstack.it/it-jobs?positiontype=11&location=Praha&isDetail=0"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["jobs"]
    return value


def job_check(url):
    # create a database connection
    with sqlite3.connect('jobs.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM jobs WHERE url = ?', (url,) # Execute a query to check if the URL exists.
                       )
    return cursor.fetchone() is not None


def find_new_jobs(jobs):
    """Find new vacancy jobs"""
    new_jobs=[]

    for job in jobs:
        job["company"] = job["company"] or "Unknown"
        job["created_at"] = datetime.now(timezone.utc).isoformat()

        if not job_check(job["url"]):
            new_jobs.append(job)
            add_new_job(job)  # from database.py

    return new_jobs


if __name__ == "__main__":
    create_tables()

    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        new_jobs = find_new_jobs(extracted)
        if new_jobs:
            print("New vacancy found")
            print(new_jobs)
        else:
            print("No new jobs found")
        time.sleep(3600)
