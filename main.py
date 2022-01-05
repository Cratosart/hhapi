import requests
prog={}
top_programming_language = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "C#", "C"]

for language in top_programming_language:
    url = 'https://api.hh.ru/vacancies'
    payload = {'text': language,
               'area': '1',
                'period': '30'}
    info = requests.get(url, params=payload)
    counter = info.json()['found']
    prog[language] = counter
    print(prog)
    test2 = info.json()['items']
    for work in test2:
        print(work['name'])
        print(work['salary'])


    # "items": [
    #     {
    #         "id": "48457284",
    #         "premium": false,
    #         "name": "Разработчик Solidity/Разработчик Rust/Разработчик Go/Разработчтик python(удаленно)",
    #         "department": null,
    #         "has_test": false,
    #         "response_letter_required": false,
    #         "area": {
    #             "id": "1",
    #             "name": "Москва",
    #             "url": "https://api.hh.ru/areas/1"
    #         },
    #         "salary": {
    #             "from": 600000,
    #             "to": null,
    #             "currency": "RUR",
    #             "gross": false

