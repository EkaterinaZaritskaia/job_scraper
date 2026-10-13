# job_scraper
![Tests](https://github.com/EkaterinaZaritskaia/job_scraper/actions/workflows/tests.yml/badge.svg)

> 🚧 Work in progress

A Python script that checks jobstack.it every hour, stores vacancies in a local SQLite database and reports only new ones.

**Stack:** Python 3.12, requests, selectorlib, SQLite, pytest

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Test

```bash
pytest -v
```

## Roadmap

- [x] Scrape and parse job listings
- [x] Store jobs in SQLite, detect new ones by URL
- [x] Unit tests for the database layer
- [x] Isolate tests with pytest `tmp_path`
- [x] GitHub Actions CI
- [ ] Notifications about new jobs (e.g. email / Telegram)
