const axios = require('axios').default;
const jsdom = require('jsdom');

const { writeToCsv } = require('./writer');

const { JSDOM } = jsdom;

let i = 0;
let fileNumber = 1;
const failedMovies = [];

module.exports.parsePage = async (username) => {
    try {
        const lastPage = await getLastPage(username);
        console.group(lastPage);
        for (let page = 1; page <= parseInt(lastPage); page++) {
            parse(username, page);
        }
        console.log(failedMovies);
        
    } catch (error) {
        console.log('parsePage error', error.response);
    }
}

const getLastPage = async (username) => {
    try {
        const response = await axios.get(`https://filmow.com/usuario/${username}/filmes/ja-vi/`);
        const { document } = new JSDOM(response.data).window;
        const pages = document.querySelectorAll('.pagination ul li a');
        const lastPageHref = pages[pages.length - 1].href;
        const lastPage = lastPageHref.match(/pagina=(\w+)/)[1];
        return lastPage;
    } catch (error) {
        console.log('getLastPage error', error.response);
    }
}

const parse = async (username, page) => {
    try {
        const response = await axios.get(`https://filmow.com/usuario/${username}/filmes/ja-vi?pagina=${page}`);
        const { document } = new JSDOM(response.data).window;
        const movies = document.querySelectorAll('li.movie_list_item');
        movies.forEach(movie => {
            const userRatingSelector = movie.querySelector('.user-rating .average');
            const userRating = userRatingSelector ? userRatingSelector.getAttribute('style') : null;
            const rating = calculateUserRating(userRating);
            parseMovie(movie.querySelector('.wrapper a.tip-movie').href, rating);
        });
    } catch (error) {
        console.log('parse error', error.response);
    }
}

const calculateUserRating = (userRating) => {
    if (typeof userRating === 'string') {
        const totalRating = userRating.match(/width: (.*?).0%/)[1];
        const ratingOutOf5 = totalRating / 20;
        return ratingOutOf5;
    }
}

const parseMovie = async (href, rating) => {
    try {
        const response = await axios.get('http://www.filmow.com' + href);
        const { document } = new JSDOM(response.data).window;
        const parsedPage = parsePage(document);
        i += 1
        if (i >= 1900) {
            fileNumber += 1;
            i = 0;
        }
        writeToCsv([...parsedPage, rating], fileNumber);
    } catch (error) {
        if (error.message === 'read ECONNRESET') {
            failedMovies.push(error.config.url);
        }
        if (error.message === 'getaddrinfo ENOTFOUND www.filmow.com www.filmow.com:443') {
            try {
                const response = await axios.get('https://www.filmow.com' + href);
                const { document } = new JSDOM(response.data).window;
                const parsedPage = parsePage(document);
                i += 1
                if (i >= 1900) {
                    fileNumber += 1;
                    i = 0;
                }
                writeToCsv(parsedPage, fileNumber);
            } catch (err) {
                console.log('caralho deu ruim mesmo', err);
            }
        }
    }
}

const parsePage = (document) => {
    const title = document.querySelector('h2.movie-original-title')
        ? document.querySelector('h2.movie-original-title').innerHTML
        : document.querySelector('h1');
    const directors = document.querySelector('.directors span strong')
        ? document.querySelector('.directors span strong').innerHTML
        : '';
    const year = document.querySelector('small.release')
        ? document.querySelector('small.release').innerHTML
        : '';
    return [title, directors, year, calculateUserRating(rating)];
}