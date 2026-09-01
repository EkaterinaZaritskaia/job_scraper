import sqlite3
import pytest

from database import create_tables, add_new_job


@pytest.fixture
def database():
    create_tables("jobs_test.db")

    with sqlite3.connect('jobs_test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs")
        conn.commit()

    yield

    with sqlite3.connect('jobs_test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs")
        conn.commit()


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


def test_add_new_job(database):
    job = create_test_job()

    add_new_job(job, "jobs_test.db")

    result = find_job_by_url(job["url"])

    assert result is not None


def test_find_missing_job(database):
    result = find_job_by_url("/test-job/321")

    assert result is None


def test_unique_job(database):
    job = create_test_job()

    add_new_job(job, "jobs_test.db")

    with pytest.raises(sqlite3.IntegrityError):
        add_new_job(job, "jobs_test.db")