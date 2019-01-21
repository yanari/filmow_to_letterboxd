import os
import csv
import string
import requests
import re
from bs4 import BeautifulSoup

page = 1
total_files = 1
soup = BeautifulSoup(features='html.parser')

def get_last_page(user):
  url = 'https://filmow.com/usuario/'+ user + '/filmes/ja-vi/?pagina=2'

  source_code = requests.get(url).text

  soup = BeautifulSoup(source_code, 'html.parser')

  tag = list(soup.find('div', {'class': 'pagination'}).find('ul').children)[-2]
  match = re.search(r'pagina=(\d*)', str(tag)).group(1)
  return int(match)

def parse(user):
  page = 1
  last_page = get_last_page(user)

  while page <= last_page:
    url = 'https://filmow.com/usuario/'+ user + '/filmes/ja-vi/?pagina=' + str(page)

    source_code = requests.get(url).text

    soup = BeautifulSoup(source_code, 'html.parser')

    for title in soup.find_all('a', {'class': 'tip-movie'}):
      parse_movie('https://filmow.com' + title.get('href'))
      global movies_parsed
      movies_parsed += 1
    page += 1

def write_to_csv(movie):
  global total_files
  global movies_parsed
  if movies_parsed < 1900:
    with open(str(total_files) + '.csv', 'a', encoding='UTF-8') as f:
      writer = csv.writer(f)
      writer.writerow((
        movie['title'],
        movie['director'],
        movie['year']
      ))
  else:
    total_files += 1
    create_csv(total_files)


def create_csv(all_movies):
  with open(str(all_movies) + '.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(('Title', 'Directors', 'Year'))

def parse_movie(url):
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
    movie['year'] = ' '

  print(movie['title'] + ' adicionado.')
  write_to_csv(movie)

def main():
  global movies_parsed

  global total_files

  movies_parsed = 0
  total_files = 1


  create_csv(total_files)
  user = input('Seu nome de usuário: ')
  parse(user)

if __name__ == "__main__":
  main()
  