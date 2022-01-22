import os
import requests
import time

from itertools import count
from terminaltables import AsciiTable


def predict_rub_salary_from_hh(vacancy):
    salary = vacancy['salary']
    if not salary or not salary['currency'] == 'RUR':
        return None
    wage = calculate_average_salary(
        salary['from'],
        salary['to']
        )
    return wage



def predict_rub_salary_for_superJob(vacancy):
    if vacancy['currency'] == 'rub':
        wage = calculate_average_salary(
            vacancy['payment_from'],
            vacancy['payment_to']
        )
        return wage


def calculate_average_salary(of, to):
    if of and to:
        wage = (of + to)/2
        return wage
    elif not to:
        wage = of*1.2
        return wage
    elif not of and to:
        wage = to*0.8
        return wage


def create_table(vacancies, title):
    columns = [['Язык программирования',
                   'Вакансий найдено',
                   'Вакансий использовано',
                   'Средняя зарплата']]
    for language, statistics in vacancies.items():
        columns.append([
            language,
            statistics['vacancies_found'],
            statistics['vacancies_processed'],
            int(statistics['average_salary'])
        ])
        table = AsciiTable(columns, title)
        table.inner_row_border = True
    return table.table


def get_from_hh(url, language):
    salary = []
    page = 0
    headers = {
        'User-Agent': 'api-test-agent'
    }
    payload = {
        'text': language,
        'area': '1',
        'period': '30',
        'page': page
    }
    for page in count(0):
        time.sleep(0.3)
        info = requests.get(
            url,
            headers=headers,
            params=payload
        )
        info.raise_for_status()

        collected = info.json()
        vacancies_found = collected['found']
        vacancies = collected['items']
        if page >= collected['pages']-1:
            break
        for job_vacancy in vacancies:
            wage = predict_rub_salary_from_hh(job_vacancy)
            if wage:
                salary.append(wage)
    if salary:
        total = sum(salary) / len(salary)
    else:
        total = 0

    return {'vacancies_found': vacancies_found,
            'vacancies_processed': len(salary),
            'average_salary': total
            }



def get_from_sj(url, language, API_KEY):
    money = []
    headers = {
        'X-Api-App-Id': API_KEY
    }
    payload = {
        'keyword': f'Программист {language}',
        'geo[t][0]': 4,
    }
    for page in count(0):
        payload['page'] = page
        job_sj = requests.get(url, headers=headers, params=payload)
        job_sj.raise_for_status()
        collected = job_sj.json()
        vacancies_found = collected['total']
        info = collected['objects']
        for job in info:
            salary = (predict_rub_salary_for_superJob(job))
            if salary is not None:
                money.append(salary)
        if not collected['more']:
            break
    if money:
        total = sum(money) / len(money)
    else:
        total = 0

    return {
        'vacancies_found': vacancies_found,
        'vacancies_processed': len(money),
        'average_salary': total
    }



if __name__ == '__main__':
    api_key_sj = os.environ['API_KEY_SJ']
    statistics = {}
    statistics_sj = {}
    top_programming_language = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C'
    ]
    url_hh = 'https://api.hh.ru/vacancies'
    url_sj = 'https://api.superjob.ru/2.0/vacancies/'
    for language in top_programming_language:
        statistics[language] = get_from_hh(
            url_hh,
            language
        )
        statistics_sj[language] = get_from_sj(
            url_sj,
            language,
            api_key_sj
        )
    print(create_table(
        statistics,
        'Work on HeadHunter Moscow'
    ))
    print(create_table(
        statistics_sj,
        'Work on SuperJob Moscow'
    ))
