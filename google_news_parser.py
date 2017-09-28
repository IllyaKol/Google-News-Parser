#!/usr/bin/python3

import csv
import urllib.request
from bs4 import BeautifulSoup

# Новини двох країн
FIRST_URL = 'https://news.google.com/news/?ned=uk_ua&hl=uk'
SECOND_URL = 'https://news.google.com/news/headlines?ned=au&hl=en-AU'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html)
    sections = soup.find('div', class_='JPdR6b Zdjuef')

    url_sections = []
    projects = []

    # Отримую всі силкі на тематичні розділи(ліва колонка)
    for section_row in sections.find_all('a', href=True)[:-1]:
        url_sections.append('https://news.google.com/news/' + section_row['href'])

    for url in url_sections:
        page_html = get_html(url)
        soup_page = BeautifulSoup(page_html)

        # Дістаю секцію та країну
        title = soup_page.find('h1', class_='oEoZRe').span.text
        country = soup_page.find('div', class_='MocG8c yR6cfb LMgvRb KKjvXb').content.text.split()[0]

        # Створюю список всіх сюжетів
        url_story = []

        # Знаходжу url і додаю у список
        rows = soup_page.find('div', class_='deQdld')
        for row in rows.find_all('div', class_='jJzAOb'):
            all_story = row.find('a', class_='FKF6mc TpQm9d', href=True)
            url_story.append('https://news.google.com/news/' + all_story.attrs['href'])

        # Проходжусь по кожній темі, беру силку та видавництво
        for story in url_story:
            story_html = get_html(story)
            soup_story = BeautifulSoup(story_html)

            story_rows = soup_story.find('div', class_='KaRWed XogBlf')
            for story_row in story_rows.find_all('c-wiz', class_='lPV2Xe k3Pzib Kckm1e'):
                all_url_story = story_row.find('a', class_='nuEeue hzdq5d ME7ew', href=True)

                # Роблю виключення
                try:
                    all_url = all_url_story.attrs['href']
                except:
                    all_url = ''

                try:
                    publishing_by = story_row.find('span', class_='IH8C7b Pc0Wt').text
                except:
                    publishing_by = ''

                projects.append({
                    'publishing_by': publishing_by,
                    'url': all_url,
                    'country': country,
                    'title': title
                })
    return projects


def save(projects, path):
    with open(path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Publishing by', 'URL', 'Country', 'Section'))

        for project in projects:
            writer.writerow((project['publishing_by'], project['url'], project['country'], project['title']))


def main():
    data = parse(get_html(FIRST_URL)) + parse(get_html(SECOND_URL))
    save(data, 'csv_file.csv')


if __name__ == '__main__':
    main()
