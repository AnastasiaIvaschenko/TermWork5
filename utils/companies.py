import requests

def get_companies():
    url = 'https://api.hh.ru/employers'
    key = input("Введите словосочетание для области поиска вакансий")
    params = {'text': key, 'area': 113}
    response = requests.get(url, params=params)
    data = response.json()

    companies = []

    for item in data['items'][:50]:
        employer_id = item['id']
        companies.append(int(employer_id))

    return companies

# print(get_companies())