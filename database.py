import sqlite3

def create_tables():
    #  the CREATE TABLE statements that create the jobs table:
    sql_statements = ['''CREATE TABLE IF NOT EXISTS jobs(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        company TEXT NOT NULL,
                                        title TEXT NOT NULL,
                                        url TEXT NOT NULL UNIQUE,
                                        created_at TEXT NOT NULL
                                        )
                                        ''']
    # create a database connection
    try:
        with sqlite3.connect('jobs.db') as conn:
            cursor = conn.cursor()

            for statement in sql_statements:
                cursor.execute(statement)

        conn.commit()
        print("Tables created successfully.")

    except sqlite3.OperationalError as e:
       print("Failed to create tables:", e)


def add_new_job(job):
    # insert table statement
    sql = '''
        INSERT INTO jobs(
        company, 
        title, 
        url, 
        created_at)
        VALUES(?, ?, ?, ?)'''


    with sqlite3.connect('jobs.db') as conn:
        cursor = conn.cursor()

        cursor.execute(sql,(
                        job['company'],
                        job['title'],
                        job['url'],
                        job['created_at']))
        conn.commit()