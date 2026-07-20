import argparse
import csv
import os
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

import cloudscraper
from bs4 import BeautifulSoup
from colorama import Fore, Style, just_fix_windows_console


BASE_URL = "https://filmow.com"
CSV_COLUMNS = ("Title", "Directors", "Year", "Rating")
CSV_LIMIT = 1900
USE_COLORS = sys.stdout.isatty() and "NO_COLOR" not in os.environ


def color(text, ansi_color):
    if not USE_COLORS:
        return text
    return f"{ansi_color}{text}{Style.RESET_ALL}"


def get_page(session, url):
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_last_page(soup):
    pages = [
        int(page)
        for link in soup.select(".pagination a[href]")
        if (match := re.search(r"pagina=(\d+)", link["href"]))
        for page in [match.group(1)]
    ]
    return max(pages, default=1)


def get_movie(session, path, rating):
    soup = get_page(session, urljoin(BASE_URL, path))
    title_element = soup.select_one(".movie__title")
    if not title_element:
        raise ValueError("título não encontrado")

    title = title_element.get_text(strip=True)
    original_title = soup.select_one(
        "div.col-12.col-xl-7 > div.d-flex.gap-2 span i"
    )
    if original_title:
        title = original_title.get_text(strip=True)

    directors = [
        link.get_text(strip=True)
        for link in soup.select(".movie__mobile-directors a")
    ]

    year_element = soup.select_one(".movie__year")
    year_match = re.search(r"\d{4}", year_element.get_text()) if year_element else None

    return {
        "Title": title,
        "Directors": ", ".join(directors),
        "Year": year_match.group() if year_match else "",
        "Rating": rating or "",
    }


def get_movies(username):
    session = cloudscraper.create_scraper()
    watched_url = f"{BASE_URL}/usuario/{username}/filmes/ja-vi/"
    first_page = get_page(session, watched_url)

    if not first_page.select_one("#movies-list"):
        raise ValueError(f"usuário '{username}' não encontrado ou sem filmes assistidos")

    total_element = first_page.select_one('a.stat[href*="/filmes/ja-vi/"] .number')
    if not total_element:
        raise ValueError(f"não foi possível obter o total de filmes de '{username}'")
    total_movies = int(total_element.get_text(strip=True))

    print("--------------------------------")
    print(
        color(
            f"Usuário {username} encontrado. "
            f"Total de filmes a serem importados: {total_movies}",
            Fore.CYAN,
        )
    )
    print("--------------------------------")

    movies = []
    total_pages = get_last_page(first_page)

    for page_number in range(1, total_pages + 1):
        print(color(f"Página {page_number}/{total_pages}", Fore.MAGENTA))
        soup = (
            first_page
            if page_number == 1
            else get_page(session, f"{watched_url}?pagina={page_number}")
        )

        for item in soup.select("#movies-list li.movie_list_item"):
            link = item.select_one("a.tip-movie[href]")
            if not link:
                continue

            rating_element = item.select_one(".star-rating[title]")
            rating_match = (
                re.search(r"Nota: ([0-5](?:\.5)?)", rating_element["title"])
                if rating_element
                else None
            )

            try:
                movie = get_movie(
                    session,
                    link["href"],
                    rating_match.group(1) if rating_match else None,
                )
                movies.append(movie)
                rating = (
                    color(f"Nota {movie['Rating']}", Fore.GREEN)
                    if movie["Rating"]
                    else color("Nota não atribuída", Fore.YELLOW)
                )
                print(f"{movie['Title']} - {rating}")
            except Exception as error:
                print(
                    color(
                        f"Aviso: não foi possível importar {link['href']}: {error}",
                        Fore.YELLOW,
                    )
                )

    if not movies:
        raise RuntimeError("nenhum filme foi importado; nenhum CSV foi criado")

    return movies


def write_csv_files(username, movies, output_directory):
    output_directory.mkdir(parents=True, exist_ok=True)
    files = []
    chunks = [
        movies[index : index + CSV_LIMIT]
        for index in range(0, len(movies), CSV_LIMIT)
    ]

    for number, chunk in enumerate(chunks, start=1):
        suffix = f"-{number}" if len(chunks) > 1 else ""
        path = output_directory / f"{username}{suffix}.csv"
        with path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(chunk)
        files.append(path)

    return files


def main():
    just_fix_windows_console()
    parser = argparse.ArgumentParser(
        description="Exporta filmes assistidos do Filmow para CSV do Letterboxd."
    )
    parser.add_argument("usuario", help="nome de usuário no Filmow")
    parser.add_argument(
        "-o",
        "--saida",
        type=Path,
        default=Path.cwd(),
        help="pasta de saída (padrão: pasta atual)",
    )
    args = parser.parse_args()
    username = args.usuario.strip().lower()

    try:
        files = write_csv_files(username, get_movies(username), args.saida)
    except Exception as error:
        print(color(f"Erro: {error}", Fore.RED), file=sys.stderr)
        return 1

    print(color("\nConcluído:", Fore.GREEN))
    for path in files:
        print(path.resolve())
    print("Importe o(s) CSV(s) em https://letterboxd.com/import/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())