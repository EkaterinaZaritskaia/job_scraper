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


def create_test_job(company="Test Company", title="QA Engineer", url="/test-job/123", created_at="2026-08-01T00:00:00"):
    job = {
        "company": company,
        "title": title,
        "url": url,
        "created_at": created_at
    }
    return job


def find_job_by_url(url):
    with sqlite3.connect('jobs_test.db') as conn:
        cursor = conn.cursor() #processes the request

        cursor.execute("SELECT * FROM jobs WHERE url = ?", (url,),)

        result = cursor.fetchone()

    return result


def test_create_tables(database):
    create_tables("jobs_test.db")

    with sqlite3.connect("jobs_test.db") as conn:
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(jobs)")
        result = cursor.fetchall()

        column_names = [item[1] for item in result]

        assert column_names == ["id", "company", "title", "url", "created_at"]

#        print(column_names)

def test_add_new_job(database):
    job = create_test_job()

    add_new_job(job, "jobs_test.db")

    result = find_job_by_url(job["url"])

    assert result is not None
    assert result[1] == job["company"]
    assert result[2] == job["title"]
    assert result[4] == job["created_at"]
 

def test_find_missing_job(database):
    result = find_job_by_url("/test-job/321")

    assert result is None

#Prohibit duplicate URLs
def test_unique_job(database):
    job = create_test_job()

    add_new_job(job, "jobs_test.db")

    with pytest.raises(sqlite3.IntegrityError):
        add_new_job(job, "jobs_test.db")


def test_add_job_without_company(database):
    job = create_test_job(company=None)
    with pytest.raises(sqlite3.IntegrityError):
        add_new_job(job, "jobs_test.db")


def test_job_without_title(database):
    job = create_test_job(title=None)
    with pytest.raises(sqlite3.IntegrityError):
        add_new_job(job, "jobs_test.db")


def test_job_without_url(database):
    job = create_test_job(url=None)
    with pytest.raises(sqlite3.IntegrityError):
        add_new_job(job, "jobs_test.db")


def test_job_without_created_at(database):
    job = create_test_job(created_at=None)
    with pytest.raises(sqlite3.IntegrityError):
        add_new_job(job, "jobs_test.db")