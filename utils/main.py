import requests
from companies import get_companies
from dbmanager import DBManager

def get_vacancies(): #query - ключевое слово поиска #page - position
    for employer_id in get_companies():
        employers = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        vacancies = requests.get(f'https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=50')
