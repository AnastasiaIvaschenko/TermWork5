import psycopg2

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='postgres', user='postgres', password='password', host='localhost',
                                     port=5432)

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                             CREATE TABLE IF NOT EXISTS companies (
                             company_id SERIAL PRIMARY KEY,
                             company_name TEXT NOT NULL,
                             url TEXT NOT NULL
                             );
        """)
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS vacancies (
                            vacancy_id SERIAL PRIMARY KEY,
                            vacancy_name TEXT NOT NULL,
                            company_id INTEGER REFERENCES companies(company_id),
                            salary_min INTEGER,
                            salary_max INTEGER,
                            url TEXT NOT NULL
                            );
        """)
        self.conn.commit()

    def drop_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS vacancies;")
        cursor.execute("DROP TABLE IF EXISTS companies;")
        self.conn.commit()

    def insert_data(self, companies, vacancies):
        cursor = self.conn.cursor()
        # Сохраняем данные работодателя в таблицу employers
        cursor.execute(f"""INSERT INTO companies (company_id, company_name, url)
        VALUES(%s, %s, %s)""", (int(companies['id']), companies['name'], companies['alternate_url'])
                       )

        self.conn.commit()

        # Сохраняем данные о вакансиях в таблицу vacancies
        for vacancy in vacancies['items']:
            cursor.execute(f"""INSERT INTO vacancies (vacancy_id, vacancy_name, company_id, salary_min, salary_max, url)
                    VALUES(%s, %s, %s, %s, %s, %s)""", (int(vacancy['id']) if vacancy['id'] != None else None,
                                                        vacancy['name'] if vacancy['name'] != None else 'NULL',
                                                        int(vacancy['employer']['id']),
                                                        int(vacancy['salary']['from']) if vacancy['salary'] and
                                                                                          vacancy['salary']['from'] != None
                                                                                   else None,
                                                        int(vacancy['salary']['to']) if vacancy['salary'] and
                                                                                          vacancy['salary']['to'] != None
                                                                                   else None,
                                                        vacancy['alternate_url'] if vacancy['alternate_url'] != None
                                                                               else 'NULL'
                                                        )
                           )
            self.conn.commit()

    def get_companies_and_vacancies_count(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT companies.company_name, COUNT(vacancies.company_id)
        FROM companies
        JOIN vacancies USING(company_id)
        GROUP BY companies.company_name
        """)
        return cursor.fetchall()

    def get_all_vacancies(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT companies.company_name, vacancies.vacancy_name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM companies
        JOIN vacancies USING(company_id)
        """)
        return cursor.fetchall()

    def get_avg_salary(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT AVG(salary_max)
        FROM vacancies
        """)
        return cursor.fetchone()

    def get_vacancies_with_higher_salary(self):
        # avg_salary = float(self.get_avg_salary()[0])
        cursor = self.conn.cursor()
        cursor.execute(f"""
        SELECT companies.company_name, vacancies.vacancy_name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM companies
        JOIN vacancies USING(company_id)
        WHERE vacancies.salary_max > ({float(self.get_avg_salary()[0])})
        """)
        return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute(f"""
        SELECT companies.company_name, vacancies.vacancy_name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM companies
        JOIN vacancies USING(company_id)
        WHERE vacancies.vacancy_name LIKE '%{keyword}%'
        """)
        return cursor.fetchall()

# db = DBManager()
# print(db.get_vacancies_with_higher_salary())
