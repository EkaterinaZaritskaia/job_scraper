import requests
import selectorlib

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

def load_new_job():
    """Creation of the .txt file"""
    try:
        with open("data.txt", "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

def save_new_job(job):
    """Save data to the .txt file"""
    with open("data.txt", "a", encoding = "utf-8") as file:
        file.write(f'{job["title"]} | {job["url"]}\n')

def find_new_jobs(jobs):
    """Find new vacancy jobs"""
    seen_jobs = load_new_job()

    new_jobs=[]

    for job in jobs:
        if f'{job["title"]} | {job["url"]}' not in seen_jobs:
            new_jobs.append(job)
            save_new_job(job)
    return new_jobs

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    new_jobs = find_new_jobs(extracted)
    if new_jobs:
        print("New vacancy found")
        print(new_jobs)
    else:
        print("No new jobs found")
