import logging
import webbrowser
import dataclasses as dc

import requests
import regex as re
import pandas as pd
from bs4 import BeautifulSoup


log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


@dc.dataclass
class Parser:
    user: str
    base_url: str = dc.field(init=False)
    movies: list[dict[str, str]] = dc.field(init=False, default_factory=list)

    def __post_init__ (self) -> None:
        self.base_url = f"https://filmow.com/usuario/{self.user}/filmes/ja-vi/"

        self.parse()
        self.write_csv_files()

    def get_last_page (self) -> int:
        last_page = 1

        source_code = requests.get(self.base_url).text
        soup = BeautifulSoup(source_code, "html.parser")

        try:
            pag_div = soup.find("div", class_="pagination")
            u_list = pag_div.find("ul").find_all("li")
            for li in u_list:
                match = re.search(r"pagina=(\d*)", str(li)).group(1)
                last_page = max(last_page, int(match))

        except Exception:
            log.info("Erro ao tentar encontrar a última página.")
            pass

        return last_page

    def parse (self) -> None:
        curr_page = 1
        last_page = self.get_last_page()

        while curr_page <= last_page:
            url = self.base_url + f"?pagina={curr_page}"
            source_code = requests.get(url).text
            soup = BeautifulSoup(source_code, "html.parser")

            if soup.find("h1").text == "Vixi! - Página não encontrada":
                log.info(f"Erro ao tentar acessar a {curr_page}-ésima página do ja-vi.")
                raise Exception

            movie_list = soup.find("ul", id="movies-list").find_all("li")
            for movie in movie_list:
                title = movie.find("a", class_="tip-movie")["href"]
                rating = None

                try:
                    star_span = movie.find("span", class_="star-rating")
                    rating = re.match(
                        r"Nota: ([0-5](?:\.5)?) estrela(?:s)?", star_span["title"]
                    ).group(1)

                except Exception:
                    pass

                self.parse_movie(title, rating)

            curr_page += 1

    def parse_movie (self, movie_title, rating: str | None) -> None:
        log.debug(f"Iniciando leitura do filme {movie_title}")

        source_code = requests.get(f"https://filmow.com{movie_title}").text
        soup = BeautifulSoup(source_code, "html.parser")

        try:
            movie_profile = soup.find("div", class_="movie-profile")
            title_div = movie_profile.find("div", class_="movie-title")
            title = title_div.find("h1").text

            if (
                original_name := movie_profile.find("h2", class_="movie-original-title")
            ) is not None:
                title = original_name.text

            else:
                log.debug("\tUtilizando título em português.")

            director = None
            try:
                directors = movie_profile.find("div", class_="directors").find_all("a")
                director = ", ".join([
                    director.find("span", itemprop="name").getText().strip()
                    for director in directors
                ])

            except Exception:
                log.debug("\tDiretor não encontrado.")
                pass

            release = None
            try:
                release = title_div.find("small", class_="release").text

            except Exception:
                log.debug("\tAno de Lançamento não encontrado.")
                pass

            if rating is None:
                log.debug("\tRating não identificado para o filme")

            self.movies.append({
                "Title": title,
                "Directors": director,
                "Year": release,
                "Rating": rating,
            })

        except Exception:
            log.debug(f"Erro tentando ler o filme referente a {movie_title}")
            pass

    def write_csv_files (self) -> None:
        df = pd.DataFrame(self.movies, columns=["Title", "Directors", "Year", "Rating"])

        curr_file = 1
        start_index = 0
        end_index = min(1900, len(self.movies))

        while end_index < len(self.movies):
            df[ start_index : end_index ].to_csv(
                f"{curr_file} + {self.user}.csv", index=False, encoding="UTF-8"
            )

            start_index = end_index
            end_index = min(start_index + 1900, len(self.movies))
            curr_file += 1

        df[ start_index : end_index ].to_csv(
            f"{curr_file} + {self.user}.csv", index=False, encoding="UTF-8"
        )


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
        go_to_letterboxd = input(
            'Gostaria de ser direcionado para "https://letterboxd.com/import/"? (s/n) '
        ).lower()
        if not go_to_letterboxd == "" and go_to_letterboxd[0] in ("s", "n"):
            break

        else:
            print("Opcao inválida.")

        if go_to_letterboxd.startswith("s"):
            webbrowser.open("https://letterboxd.com/import/")

        else:
            print("Então tchau")
