import os
import csv
import string
import requests
import re
from bs4 import BeautifulSoup

class Parser():
  def __init__(self, user):
    self.page = 1
    self.total_files = 1
    self.movies_list = []
    self.soup = BeautifulSoup(features='html.parser')

    self.movies_parsed = 0
    self.total_files = 1
    self.user = user

    self.create_csv(self.total_files)
    self.parse(self.user)

  def get_last_page(self, user):
    url = 'https://filmow.com/usuario/'+ user + '/filmes/ja-vi/'

    source_code = requests.get(url).text

    soup = BeautifulSoup(source_code, 'html.parser')

    try:
      tag = list(soup.find('div', {'class': 'pagination'}).find('ul').children)[-2]
      match = re.search(r'pagina=(\d*)', str(tag)).group(1)
      return int(match)
    except:
      return 1

  def parse(self, user):
    self.page = 1
    last_page = self.get_last_page(user)

    while self.page <= last_page:
      url = 'https://filmow.com/usuario/'+ user + '/filmes/ja-vi/?pagina=' + str(self.page)

      source_code = requests.get(url).text

      soup = BeautifulSoup(source_code, 'html.parser')

      if soup.find('h1').text == 'Vixi! - Página não encontrada':
        print(soup.find('h1'))
        raise Exception

      for title in soup.find_all('a', {'class': 'tip-movie'}):
        self.parse_movie('https://filmow.com' + title.get('href'))
        self.movies_parsed += 1
      self.page += 1

  def write_to_csv(self, movie):
    if self.movies_parsed < 1900:
      with open(str(self.total_files) + '.csv', 'a', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow((
          movie['title'],
          movie['director'],
          movie['year']
        ))
    else:
      self.total_files += 1
      self.create_csv(self.total_files)


  def create_csv(self, all_movies):
    with open(str(all_movies) + '.csv', 'w', encoding='UTF-8') as f:
      writer = csv.writer(f)
      writer.writerow(('Title', 'Directors', 'Year'))

  def parse_movie(self, url):
    movie = {'title': None, 'director': None, 'year': None}
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')

    try:
      movie['title'] = soup.find('h2', {'class': 'movie-original-title'}).get_text().strip()
    except AttributeError:
      movie['title'] = soup.find('h1').get_text().strip()

    try:
      movie['director'] = soup.find('span', {'itemprop': 'director'}).select('strong')[0].get_text()
    except AttributeError:
      try:
        movie['director'] = soup.find('span', {'itemprop': 'directors'}).getText().strip()
      except AttributeError:
        movie['director'] = ''

    try:
      movie['year'] = soup.find('small', {'class': 'release'}).get_text()
    except AttributeError:
      movie['year'] = ''

    self.write_to_csv(movie)
    self.movies_list.append(movie['title'])
    