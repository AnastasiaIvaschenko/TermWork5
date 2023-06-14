DROP TABLE IF EXISTS vacancies;
DROP TABLE IF EXISTS companies;

CREATE TABLE IF NOT EXISTS companies (
                             company_id SERIAL PRIMARY KEY,
                             company_name TEXT NOT NULL,
                             url TEXT NOT NULL
                             );

CREATE TABLE IF NOT EXISTS vacancies (
                            vacancy_id SERIAL PRIMARY KEY,
                            vacancy_name TEXT NOT NULL,
                            company_id INTEGER REFERENCES companies(company_id),
                            salary_min INTEGER,
                            salary_max INTEGER,
                            url TEXT NOT NULL
                            );

INSERT INTO companies (company_id, company_name, url) VALUES(%s, %s, %s);

INSERT INTO vacancies (vacancy_id, vacancy_name, company_id, salary_min, salary_max, url)
VALUES(%s, %s, %s, %s, %s, %s);

SELECT companies.company_name, COUNT(vacancies.company_id)
        FROM companies
        JOIN vacancies USING(company_id)
        GROUP BY companies.company_name;

SELECT companies.company_name, vacancies.vacancy_name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM companies
        JOIN vacancies USING(company_id);

SELECT AVG(salary_max)
        FROM vacancies;

SELECT companies.company_name, vacancies.vacancy_name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM companies
        JOIN vacancies USING(company_id)
        WHERE vacancies.salary_max > ({float(self.get_avg_salary()[0])});

SELECT companies.company_name, vacancies.vacancy_name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM companies
        JOIN vacancies USING(company_id)
        WHERE vacancies.vacancy_name LIKE '%keyword%';

