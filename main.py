import os
import requests

from itertools import count
from terminaltables import AsciiTable


def predict_rub_salary(vacancy):
    salary = vacancy['salary']
    if not salary:
        return None
    if salary['currency'] == 'RUR':
        wage = calculation_salary_values(salary['from'], salary['to'])
        return wage


def predict_rub_salary_for_superJob(vacancy):
    if vacancy['currency'] == 'rub':
        wage = calculation_salary_values(vacancy['payment_from'],vacancy['payment_to'])
        if wage is not None:
            return wage


def calculation_salary_values(of, to):
    if of != 0:
        if to != 0:
            wage = (of+to)/2
            return wage
        elif to == 0:
            wage = of*1.2
            return wage
    elif of == 0 and to !=0:
        wage = to*0.8
        return wage


def create_table(dict_date, title_table):
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий использовано', 'Средняя зарплата']]
    for programming_language, statistics_data in dict_date.items():
        table_data.append([programming_language, statistics_data['vacancies_found'], statistics_data['vacancies_processed'], int(statistics_data['average_salary'])])
        title = title_table
        table = AsciiTable(table_data, title)
        table.inner_row_border = True
    return table.table


def getting_data_from_hh(url, language):
    salary = []
    for page in count(0):
        payload = {'text': language,
                       'area': '1',
                       'period': '30',
                       'page': page
                       }
        info = requests.get(url, params=payload)
        info.raise_for_status()

        collected_data = info.json
        counter = collected_data['found']
        vacancies = collected_data['items']
        if page >= collected_data['pages']-1:
            salary.clear
            break
        for job_vacancy in vacancies:
            wage = predict_rub_salary(job_vacancy)
            if wage is not None:
                salary.append(wage)

        page+=1
    total = (int(sum(salary) / (len(salary))))
    statistics[language] = {"vacancies_found": counter, "vacancies_processed": len(salary),
                      "average_salary": total}
    return statistics

def getting_data_from_sj(url, language):
    money = []
    headers = {
        'X-Api-App-Id': API_KEY_SJ
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
        if collected_data['more'] == False:
            break
        for job in info:
            salary = (predict_rub_salary_for_superJob(job))
            if salary is not None:
                money.append(salary)


        page+=1

    if money:
        total = sum(money) / len(money)
        statistics[language] = {"vacancies_found": counter, "vacancies_processed": len(money),
                                     "average_salary": total}
        return statistics_sj
    else:
        statistics_sj[language] = {"vacancies_found": counter, "vacancies_processed": 0,
                                     "average_salary": 0}
        return statistics_sj


if __name__ == '__main__':
    API_KEY_SJ = os.environ['API_KEY_SJ']
    statistics = {}
    statistics_sj = {}
    top_programming_language = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "C#", "C"]
    url_hh = 'https://api.hh.ru/vacancies'
    url_sj = 'https://api.superjob.ru/2.0/vacancies/'
    for language in top_programming_language:
        statistics = getting_data_from_hh(url_hh, language)
        statistics_sj = getting_data_from_sj(url_sj, language)
    print(create_table(prog, "Work on HeadHunter Moscow"))
    print(create_table(prog_sj, "Work on SuperJob Moscow"))