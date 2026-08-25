import sqlite3
import os

from database import create_tables, add_new_job

if os.path.exists("jobs_test.db"):
    os.remove("jobs_test.db")

def create_test_job():
    job = {
        "company": "Test Company",
        "title": "QA Engineer",
        "url": "/test-job/123",
        "created_at": "2026-08-01T00:00:00"
    }
    return job


def find_job_by_url(url):
    with sqlite3.connect('jobs_test.db') as conn:
        cursor = conn.cursor() #processes the request

        cursor.execute("SELECT * FROM jobs WHERE url = ?", (url,),)

        result = cursor.fetchone()

    return result

create_tables("jobs_test.db")

def test_add_new_job():
    job = create_test_job()

    add_new_job(job, "jobs_test.db")

    result = find_job_by_url(job["url"])

    assert result is not None