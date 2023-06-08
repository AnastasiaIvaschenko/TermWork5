import requests

def get_companies():
    url = 'https://api.hh.ru/employers'
    params = {'text': 'производство мебели', 'area': 113}
    response = requests.get(url, params=params)
    data = response.json()

    companies = []

    for item in data['items'][:10]:
        employer_id = item['id']
        companies.append(int(employer_id))

    return companies

