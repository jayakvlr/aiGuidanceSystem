import psycopg2
from datetime import datetime

class DatabaseService:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS scraped_data (
            id SERIAL PRIMARY KEY,
            link TEXT,
            content TEXT,
            scrape_date TIMESTAMP
        );
        '''
        self.cur.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, link, content):
        insert_query = '''
        INSERT INTO scraped_data (link, content, scrape_date)
        VALUES (%s, %s, %s);
        '''
        scrape_date = datetime.now()
        self.cur.execute(insert_query, (link, content, scrape_date))
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

