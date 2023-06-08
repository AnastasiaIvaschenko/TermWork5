import psycopg2

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='postgres', user='postgres', password='pastasea84', host='localhost',
                                     port='5432')

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                             CREATE TABLE IF NOT EXIST companies (
                             company_id SERIAL PRIMARY KEY,
                             company_name TEXT NOT NULL,
                             url TEXT NOT NULL
                             );
        """)
        cursor.execute("""
                            CREATE TABLE IF NOT EXIST vacancies (
                            vacancy_id SERIAL PRIMARY KEY,
                            vacancy_name TEXT NOT NULL,
                            company_id INTEGER REFERENCES companies(company_id),
                            salary_min INTEGER,
                            salary_max INTEGER,
                            url TEXT NOT NULL
                            );
        """)
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def drop_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXIST vacancies;")
        cursor.execute("DROP TABLE IF EXIST vacancies;")
# if __name__ == "__main__":
db = DBManager()
db.create_tables()


