import requests
from companies import get_companies
from dbmanager import DBManager


def get_vacancies(): # Загружает данные работодателя и его вакансии по employer_id
    db = DBManager()
    db.drop_tables()
    db.create_tables()

    for employer_id in get_companies():
        companies = requests.get(f'https://api.hh.ru/employers/{employer_id}').json()
        vacancies = requests.get(f'https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=50').json()
        db.insert_data(companies, vacancies)


    print(db.get_companies_and_vacancies_count())
    print('-------')
    print(db.get_all_vacancies())
    print('-------')
    print(db.get_avg_salary())
    print('-------')
    print(db.get_vacancies_with_higher_salary())
    print('-------')
    keyword = input('Введите слово в названии вакансий')
    print(db.get_vacancies_with_keyword(keyword))


if __name__ == '__main__':
    get_vacancies()
