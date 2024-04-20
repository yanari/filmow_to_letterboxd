import re
import csv
import requests
import webbrowser
from bs4 import BeautifulSoup
import pandas as pd
import dataclasses as dc


@dc.dataclass
class Parser:
    user: str
    page: int = dc.field(init=False)
    movies_parsed: int = dc.field(init=False, default=0)
    df: pd.DataFrame = dc.field(init=False)
    soup: BeautifulSoup = dc.field(
        init=False, default_factory=lambda: BeautifulSoup(features="html.parser")
    )

    def __post_init__ (self) -> None:
        self.df = pd.DataFrame(columns=[
            "Title", "Directors", "Year", "Rating", "WatchedDate", "Review"
        ])
        self.parse()

    def parse (self) -> None:
        self.page = 1
        last_page = self.get_last_page()

        while self.page <= last_page:
            url = "https://filmow.com/usuario/" + self.user + "/filmes/ja-vi/?pagina=" + str(self.page)

            source_code = requests.get(url).text

            soup = BeautifulSoup(source_code, "html.parser")

            if soup.find("h1").text == "Vixi! - Página não encontrada":
                raise Exception

            for title in soup.find_all("a", {"class": "tip-movie"}):
                self.parse_movie("https://filmow.com" + title.get("href"))
                self.movies_parsed += 1

            self.page += 1

    def parse_movie(self, url):
        movie = {"title": None, "director": None, "year": None}
        source_code = requests.get(url).text
        soup = BeautifulSoup(source_code, "html.parser")

        try:
            movie["title"] = soup.find("h2", {"class": "movie-original-title"}).get_text().strip()
        except AttributeError:
            movie["title"] = soup.find("h1").get_text().strip()

        try:
            movie["director"] = soup.find("span", {"itemprop": "director"}).select("strong")[0].get_text()
        except AttributeError:
            try:
                movie["director"] = soup.find("span", {"itemprop": "directors"}).getText().strip()
            except AttributeError:
                movie["director"] = ""

        try:
            movie["year"] = soup.find("small", {"class": "release"}).get_text()
        except AttributeError:
            movie["year"] = ""

        self.write_to_csv(movie)

    def write_to_csv(self, movie):
        if self.movies_parsed < 1900:
            with open(str(self.total_files) + self.user + ".csv", "a", encoding="UTF-8") as f:
                writer = csv.writer(f)
                writer.writerow((
                    movie["title"],
                    movie["director"],
                    movie["year"]
                ))
        else:
            self.total_files += 1
            self.movies_parsed = 0
            self.create_csv(self.total_files)

    def get_last_page (self) -> int:
        url = "https://filmow.com/usuario/" + self.user + "/filmes/ja-vi/"

        source_code = requests.get(url).text

        soup = BeautifulSoup(source_code, "html.parser")

        last_page = 1

        try:
            pag_div = soup.find("div", class_="pagination")
            u_list = pag_div.find("ul").find_all("li")
            for li in u_list:
                match = re.search(r"pagina=(\d*)", str(li)).group(1)

                last_page = max(last_page, int(match))

        except Exception:
            pass

        return last_page

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
        print(f"Usuário {username} não encontrado. Tem certeza que digitou certo?")
        username = input("Digite seu nome de usuário do Filmow: ")
        Parser(username.lower().strip())

    msg = """
    Pronto!
    Vá para https://letterboxd.com/import/, SELECT A FILE,
    e selecione o(s) arquivo(s) de extensão csv criado(s) pelo programa
    """
    print(msg)

    while True:
        go_to_letterboxd = input('Gostaria de ser direcionado para "https://letterboxd.com/import/"? (s/n) ').lower()
        if not go_to_letterboxd == "" and go_to_letterboxd[0] in ("s", "n"):
            break

        else:
            print("Opcao inválida.")

        if go_to_letterboxd.startswith("s"):
            webbrowser.open("https://letterboxd.com/import/")

        else:
            print('Então tchau')
