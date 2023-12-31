from celery import Celery
import requests
from tg.db import BotDB
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlite3
import random
import re
import time
import json


class Crawler:
    def __init__(self, url):
        self.url = url

    def get_soup(self):
        soup = BeautifulSoup(requests.get(self.url).text, "html.parser")
        driver = webdriver.Chrome()
        driver.get(self.url)
        source_data = driver.page_source
        soup = bs(source_data, features="html.parser")

        return soup


class C:
    def __init__(self):
        pass

    # n - количество коленьев, которое задает пользователь
    def get_link_and_parse(self, name, n):

        # получение ссылки на актера
        current_url = Parser().get_link_actor(name)
        # получение ссылок на фильмы, в которых он снимался
        link_films = Parser().get_info_actor(current_url, current_url)
        links_emp = []

        for link in link_films:
            # получение ссылок на друзей актера
            link_employees = Parser().get_info_film(link)
            for link_emp in link_employees:
                Parser().get_info_actor(link_emp, current_url)
                links_emp.append(link_emp)
            print(links_emp)

        for _ in range(n - 1):
            links_emp = []
            for link_emp in links_emp:
                current_url = link_emp
                # получение ссылок на фильмы, в которых он снимался
                link_films = Parser().get_info_actor(link_emp, current_url)

                # обход этих ссылок по одной
                for link in link_films:
                    # получение ссылок на друзей актера
                    link_employees = Parser().get_info_film(link)
                    for link_emp in link_employees:
                        Parser().get_info_actor(link_emp, current_url)
                        links_emp.append(link_emp)
                    print(links_emp)


class Parser:
    def __init__(self):
        self.db = BotDB()

    # получение ссылки для определенного актера, имя которого вводит пользователь
    def get_link_actor(self, name):

        driver = webdriver.Chrome()
        driver.get('https://ru.kinorium.com/')
        input_tab = driver.find_element(By.CLASS_NAME, 'ui-autocomplete-input')
        input_tab.send_keys(name)
        input_tab.send_keys(Keys.ENTER)
        tab_actor = driver.find_element(By.XPATH,
                                        '/html/body/div[6]/div/div[6]/div[1]/div/div/div[2]/div/div[3]/div[1]/h3/a')
        tab_actor.send_keys(Keys.ENTER)

        return driver.current_url

    # получение информации об актерах, возвращает все ссылки фильмов, в которых снимался данный актер
    def get_info_actor(self, url, current_url):
        link_films = []
        id_films = []
        soup = Crawler(url).get_soup()
        id_actor = re.findall(r'\d+', url)
        id_current_actor = re.findall(r'\d+', url)
        if not self.db.actor_exist(id_actor[0]):
            # soup = Crawler(url).get_soup()
            time.sleep(7)

            name = soup.find('div', class_='person-page__title-elements-wrap').text.replace(u'\xa0', u' ').strip()

            try:
                birthdate = soup.find('div', class_='person_info').find('meta', itemprop='birthDate').get('content')

            except Exception as E:
                birthdate = 'no birthdate'

            try:
                gender = soup.find('div', class_='person_info').find('meta', itemprop='gender').get('content')

            except Exception as E:
                gender = 'no gender'

            for link in soup.findAll('div', class_='item headlines_type-actor'):
                link_film = 'https://ru.kinorium.com' + link.find('a', class_='filmList__item-title').get('href')
                link_films.append(link_film)
                id_films.append(re.findall(r'\d+', link_film))

            # этот массив добавлять в таблицу actor
            info_actor = [id_actor, name, gender, birthdate, id_films]
            if not self.db.actor_exist(id_actor[0]):
                if birthdate == 'no birthdate':
                    birthdate = None
                else:
                    if re.match(r'\d{4}-0{2}-00', birthdate):
                        birthdate = birthdate.replace('-00', '-01-01')
                info_actor_db = id_actor, name, gender, birthdate, id_films
                self.db.add_actor(info_actor_db)
            print(info_actor)
        else:
            for link in soup.findAll('div', class_='item headlines_type-actor'):
                link_film = 'https://ru.kinorium.com' + link.find('a', class_='filmList__item-title').get('href')
                link_films.append(link_film)
                id_films.append(re.findall(r'\d+', link_film))

        return link_films

    # получение информации о фильме, возвращает ссылки на всех людей, которые учавствовали в съёмках
    def get_info_film(self, link):

        employees = {}
        employees_db = {}
        emp_links = []
        actors = []
        info_films_db = '', '', ''
        id_film = re.findall(r'\d+', link)
        roles_to_remove = ['Режиссёр дубляжа', 'Дубляж', 'Переводчик']
        if not self.db.film_exist(id_film):
            soup = Crawler(link).get_soup()

            name = soup.find('h1', class_='film-page__title-text').text
            time.sleep(7)

            try:

                countries = []
                for country in soup.findAll('a', class_='film-page__country-link'):
                    countries.append(country.text)

                genres = []
                for genre in soup.findAll('li', itemprop='genre'):
                    genres.append(genre.text)

                warning = {}

                for par_con in soup.find('tr', class_='film-page__parentalguide-toggle-line').findAll('li'):
                    parental_control_count = par_con.find('p').text
                    parental_control = par_con.text
                    parental_control = parental_control.replace(parental_control_count, '')

                    warning[parental_control] = parental_control_count

            except Exception as E:
                warning = 'no parental control'

            # этот массив добавлять в таблицу films
            info_films = [name, link, warning, countries, genres]

            print(info_films)
            time.sleep(7)

            soup_cast = Crawler(link + 'cast').get_soup()
            for t in soup_cast.findAll('div', class_='ref-list clearfix'):
                for pos in t.findAll('h1', class_='cast-page__title'):
                    position = pos.text.strip()
                    employees[position] = []

                for emp in t.findAll('a', class_='cast-page__link-name link-info-persona-type-persona'):
                    employee = emp.get('href')
                    emp_link = 'https://ru.kinorium.com/' + employee
                    emp_links.append(emp_link)
                    employee_id = re.findall(r'\d+', employee)
                    employees[position].append(employee_id)
            info_films_db = name, id_film[0], warning, json.dumps(info_films[3]), json.dumps(info_films[4]), employees

        else:
            soup_cast = Crawler(link + 'cast').get_soup()
            for t in soup_cast.findAll('div', class_='ref-list clearfix'):
                for pos in t.findAll('h1', class_='cast-page__title'):
                    position = pos.text.strip()
                    employees[position] = []

                for emp in t.findAll('a', class_='cast-page__link-name link-info-persona-type-persona'):
                    employee = emp.get('href')
                    emp_link = 'https://ru.kinorium.com/' + employee
                    emp_links.append(emp_link)
                    employee_id = re.findall(r'\d+', employee)
                    employees[position].append(employee_id)
        for amplua, actors_temp in employees.items():
            if amplua == 'Актёры':
                actors = actors_temp
            if amplua == 'Дубляж':
                for actor in actors_temp:
                    while actor in actors:
                        actors.remove(actor)
                        emp_links.remove('https://ru.kinorium.com//name/' + actor[0] + '/')
        # keys_to_remove = []
        # for role, people in employees.items():
        #     if role in roles_to_remove:
        #         keys_to_remove.append(role)
        # print(keys_to_remove)
        # Remove keys
        # for key in keys_to_remove:
        #     employees.pop(key)
        #    print(key)

        if not self.db.film_exist(id_film):
            info_films_db = info_films_db[0:5] + (employees,)
            self.db.add_film(info_films_db)
        print(employees)
        print(emp_links)
        return emp_links


celery = Celery('celery_project', broker='redis://localhost:6379/0')


@celery.task
def parse_website(name):
    test = C().get_link_and_parse(name,1)     #поменяно было 2
    return test
