import os
import requests

from terminaltables import AsciiTable
from itertools import count


def predict_rub_salary(vacancy):
    salary = vacancy['salary']
    try:
        if salary['from'] is not None and salary['currency'] == 'RUR':
            if salary['to'] is not None:
                zarplata = (salary['from'] + salary['to']) / 2
                return zarplata
            elif salary['to'] is None:
                zarplata = salary['from'] * 1.2
                return zarplata
            else:
                return None
        elif salary['from'] is None and salary['to'] is not None:
            zarplata = salary['to'] * 0.8
            return zarplata
        else:
            return None
    except:
        return None


def predict_rub_salary_for_superJob(vacancy):
    salary = (int((vacancy['payment_from'] + vacancy['payment_to']) / 2))
    if salary is not None:
        return salary


def create_table(dict_date):
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий использовано', 'Средняя зарплата']]
    for key, value in dict_date.items():
        lang = key
        found = dict_date[key]['vacancies_found']
        proc = dict_date[key]['vacancies_processed']
        ave = int(dict_date[key]['average_salary'])
        table_data.append([lang, found, proc, ave])
    return table_data

if __name__ == '__main__':
    prog = {}
    salary = []
    top_programming_language = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "C#", "C"]

    for language in top_programming_language:
        for page in count(0):
            url = 'https://api.hh.ru/vacancies'
            payload = {'text': language,
                       'area': '1',
                       'period': '30',
                       'page': page
                       }
            info = requests.get(url, params=payload)
            info.raise_for_status()
            counter = info.json()['found']
            vacancies = info.json()['items']
            if page >= info.json()['pages'] - 1:
                salary.clear()
                break
            if language == language:
                for job_vacancy in vacancies:
                    zarplata = predict_rub_salary(job_vacancy)
                    if zarplata is not None:
                        salary.append(zarplata)
                        itog = (int(sum(salary) / (len(salary))))
                        prog[language] = {"vacancies_found": counter, "vacancies_processed": len(salary),
                                          "average_salary": itog}

        API_KEY_SJ = os.environ['API_KEY_SJ']
        prog_sj = {}
        money = []
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': API_KEY_SJ
            }
        for language in top_programming_language:
            for page in count(0):
                payload = {
                    'keyword': f'Программист {language}',
                    'geo[t][0]': 4,
                    'page': page
                }
                job_sj = requests.get(url, headers=headers, params=payload)
                job_sj.raise_for_status()
                counter = job_sj.json()['total']
                info = job_sj.json()['objects']
                if job_sj.json()['more'] == False:
                    money.clear()
                    break
                for job in info:
                    salary = (predict_rub_salary_for_superJob(job))
                    money.append(salary)
                    itog = sum(money) / len(money)
                    prog_sj[language] = {"vacancies_found": counter, "vacancies_processed": len(money), "average_salary": itog}

        table_data_sj = create_table(prog_sj)
        title = "Work on SuperJob Moscow"
        table = AsciiTable(table_data_sj, title)
        table.inner_row_border = True
        print(table.table)

        table_data_hh = create_table(prog)
        title = "Work on HeadHunter Moscow"
        table = AsciiTable(table_data_hh, title)
        table.inner_row_border = True
        print(table.table)
