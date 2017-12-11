from robobrowser import RoboBrowser
import csv
import re
import datetime

def login(usr, pwd):

    if len(pwd) > 0:
        robo = RoboBrowser(parser='html.parser')
        robo.open('https://filmow.com/login/')

        form = robo.get_form(action="/login/?next=/")
        form['username'].value = usr
        form['password'].value = pwd

        try:
            robo.submit_form(form)

            # check if the user logged in is the same as the username
            userFound = re.compile('ainel/">(.*?)</a>').search(str(robo.parsed)).group(1)
        except AttributeError:
            print('Talvez sua senha esteja errada. Tem certeza que é essa? [Tecle Enter para sair]')
            input()
            raise SystemExit

        if userFound == usr:
            print('Login sucedido!!! Carregando...\n_______________________________\n')
        else:
            print('Erro ):')

    else:
        robo = RoboBrowser(parser='html.parser')

    parseMainPage(usr, robo)

def parseMainPage(usr, driverObj):
    page = 1

    lastPage = getLastPage(usr, driverObj)

    while page <= int(lastPage):
        driverObj.open('https://filmow.com/usuario/' + usr + '/filmes/ja-vi/?pagina=' + str(page))
        parsed = driverObj.parsed
        for link in parsed.find_all('a', {'class':'cover tip-movie '}):
            linkFilm = 'https://filmow.com' + link.get('href')
            getDataFromPage(usr, linkFilm, driverObj)
        page += 1

def getLastPage(usr, driverObj):
    driverObj.open('https://filmow.com/usuario/' + usr + '/filmes/ja-vi/')

    parsed = driverObj.parsed
    lastPage = re.search('pagina=(.*)" title="última página">', str(parsed))
    if str(type(lastPage)) != '<class \'NoneType\'>':
        return int(lastPage.group(1))
    else:
        return 7


def getDataFromPage(usr, page, driverObj):

    driverObj.open(page)
    parsed = driverObj.parsed

    # ============================= GETTING TITLE ===================================
    title = parsed.find('h2', {'class', 'movie-original-title'}).getText()

    # ============================= GETTING DIRECTOR'S NAME =========================
    try:
        director = parsed.find('span', {'itemprop': 'director'}).getText().strip()
    except AttributeError:
        try:
            director = parsed.find('span', {'itemprop': 'directors'}).getText().strip()
        except AttributeError:
            director = ' '

    # ============================= GETTING RELEASE DATE ============================
    try:
        releaseDate = parsed.find('small', {'class':'release'}).text
    except AttributeError:
        releaseDate = ' '

    # ============================= GETTING RATING ==================================
    ratingResult = parsed.find('div', {'class', 'star-rating'}).get('data-average')
    if int(ratingResult) != 0:
        rating = ratingResult
    else:
        rating = ' ' # there's no user rating


    # using function writerCsv
    writerCsv(driverObj, title, director, releaseDate, rating)

def writerCsv(driverObj, title, dir, date, rating):
    parsed = driverObj.parsed

    with open(filename, 'a', encoding='UTF-8') as f:
        writer = csv.writer(f)
        try:
            writer.writerow((title, dir, date, rating))
        except UnicodeEncodeError:
            try:
                # title probably in japanese
                title = re.search('<h1 itemprop="name">(.*)</h1>', str(parsed)).group(1)
                writer.writerow((title, dir, date, rating))
            except:
                print('Nao consegui adicionar o filme', title, 'ao arquivo. ):')
def main():
    i = datetime.datetime.now()
    global filename

    usr = input('Username: ')
    print('Senha opcional, mas pra importar suas avaliacoes, é necessario fornecer a senha\n'
          '[Caso nao vá fornecer, deixe o campo em branco e tecle Enter]\n')
    pwd = input('Senha: ')

    filename = '{}_{}.{}_{}.{}.csv'.format(usr, i.day, i.month, i.hour, i.minute)

    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('Title', 'Directors', 'Year', 'Rating10'))

    login(usr, pwd)

if __name__ == '__main__':
    main()
    print('Agora vá em https://letterboxd.com/import/, clique em SELECT A FILE, e selecione o arquivo criado pelo programa :D'
          '\nEnjoy!')
