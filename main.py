import os
import requests
import time

from itertools import count
from terminaltables import AsciiTable


def predict_rub_salary_from_hh(vacancy):
    salary = vacancy['salary']
    if not salary:
        return None
    elif salary['currency'] == 'RUR':
        wage = calculate_salary_values(
            salary['from'],
            salary['to']
        )
        return wage


def predict_rub_salary_for_superJob(vacancy):
    if vacancy['currency'] == 'rub':
        wage = calculate_salary_values(
            vacancy['payment_from'],
            vacancy['payment_to']
        )
        if wage:
            return wage


def calculate_salary_values(of, to):
    if of and to:
        wage = (of + to)/2
        return wage
    elif not to:
        wage = of*1.2
        return wage
    elif not of and to:
        wage = to*0.8
        return wage


def create_table(dict_date, title_table):
    table_data = [['Язык программирования',
                   'Вакансий найдено',
                   'Вакансий использовано',
                   'Средняя зарплата']]
    for programming_language, statistics_data in dict_date.items():
        table_data.append([
            programming_language,
            statistics_data['vacancies_found'],
            statistics_data['vacancies_processed'],
            int(statistics_data['average_salary'])
        ])
        table = AsciiTable(table_data, title_table)
        table.inner_row_border = True
    return table.table


def get_data_from_hh(url, language):
    salary = []
    for page in count(0):
        time.sleep(0.3)
        headers = {
            'User-Agent': 'api-test-agent'
        }
        payload = {
            'text': language,
            'area': '1',
            'period': '30',
            'page': page
                    }
        info = requests.get(
            url,
            headers=headers,
            params=payload
        )
        info.raise_for_status()

        collected_data = info.json()
        counter = collected_data['found']
        vacancies = collected_data['items']
        if page >= collected_data['pages']-1:
            break
        for job_vacancy in vacancies:
            wage = predict_rub_salary_from_hh(job_vacancy)
            if wage:
                salary.append(wage)

        page += 1
    if salary:
        total = sum(salary) / len(salary)
    else:
        total = 0

    statistics[language] = {'vacancies_found': counter,
                            'vacancies_processed': len(salary),
                            'average_salary': total}
    return statistics


def get_data_from_sj(url, language, API_KEY):
    money = []
    headers = {
        'X-Api-App-Id': API_KEY
    }
    for page in count(0):
        payload = {
            'keyword': f'Программист {language}',
            'geo[t][0]': 4,
            'page': page
            }
        job_sj = requests.get(url, headers=headers, params=payload)
        job_sj.raise_for_status()
        collected_data = job_sj.json()
        counter = collected_data['total']
        info = collected_data['objects']
        if not collected_data['more']:
            break
        for job in info:
            salary = (predict_rub_salary_for_superJob(job))
            if salary is not None:
                money.append(salary)
        page += 1

    if money:
        total = sum(money) / len(money)
    else:
        total = 0

    statistics[language] = {
        'vacancies_found': counter,
        'vacancies_processed': len(money),
        'average_salary': total
    }
    return statistics


if __name__ == '__main__':
    API_KEY_SJ = os.environ['API_KEY_SJ']
    # statistics = {}
    # statistics_sj = {}
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
        statistics = get_data_from_hh(
            url_hh,
            language
        )
        statistics_sj = get_data_from_sj(
            url_sj,
            language,
            API_KEY_SJ
        )
    print(create_table(
        statistics,
        'Work on HeadHunter Moscow'
    ))
    print(create_table(
        statistics_sj,
        'Work on SuperJob Moscow'
    ))
