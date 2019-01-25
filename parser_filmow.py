import os
import csv
import string
import requests
import re
import webbrowser
from bs4 import BeautifulSoup

class Parser():
  def __init__(self, user):
    self.page = 1
    self.total_files = 1
    self.soup = BeautifulSoup(features='html.parser')

    self.user = user
    self.movies_parsed = 0
    self.total_files = 1

    self.parse(user)
    self.create_csv(self.total_files)

  def create_csv(self, all_movies):
    with open(str(all_movies) + self.user + '.csv', 'w', encoding='UTF-8') as f:
      writer = csv.writer(f)
      writer.writerow(('Title', 'Directors', 'Year'))
  
  def parse(self, user):
    self.page = 1
    last_page = self.get_last_page(user)

    while self.page <= last_page:
      url = 'https://filmow.com/usuario/'+ user + '/filmes/ja-vi/?pagina=' + str(self.page)

      source_code = requests.get(url).text

      soup = BeautifulSoup(source_code, 'html.parser')

      if soup.find('h1').text == 'Vixi! - Página não encontrada':
        raise Exception

      for title in soup.find_all('a', {'class': 'tip-movie'}):
        self.parse_movie('https://filmow.com' + title.get('href'))
        self.movies_parsed += 1
      self.page += 1

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

  def write_to_csv(self, movie):
    if self.movies_parsed < 1900:
      with open(str(self.total_files) + self.user + '.csv', 'a', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow((
          movie['title'],
          movie['director'],
          movie['year']
        ))
    else:
      self.total_files += 1
      self.movies_parsed = 0
      self.create_csv(self.total_files)
      
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

if __name__ == "__main__":
  try:
    username = input('Digite seu nome de usuário do Filmow: ')
    msg = """
          Seus filmes estão sendo importados no plano de fundo :)\n
          Não feche a janela e aguarde um momento.
          """
    print(msg)
    Parser(username.lower().strip())
  except Exception:
    print('Usuário {} não encontrado. Tem certeza que digitou certo?'.format(username))
    username = input('Digite seu nome de usuário do Filmow: ')
    Parser(username.lower().strip())

  msg = """
          Pronto!
          Vá para https://letterboxd.com/import/, SELECT A FILE, 
          e selecione o(s) arquivo(s) de extensão csv criado(s) pelo programa
        """
  print(msg)

  go_to_letterboxd = input('Gostaria de ser direcionado para "https://letterboxd.com/import/"? (s/n) ')

  if go_to_letterboxd.startswith('s'):
    webbrowser.open('https://letterboxd.com/import/')
  elif go_to_letterboxd.startswith('n'):
    print('Então tchau')
    input()
  else:
    print('Entendi não, mas tchau')
    input()