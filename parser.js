const axios = require('axios').default;
const jsdom = require('jsdom');

const { writeToCsv } = require('./writer');

const { JSDOM } = jsdom;

let i = 0;
let fileNumber = 1;

module.exports.parsePage = async (username) => {
    try {
        const lastPage = await getLastPage(username);
        for (let page = 1; page <= parseInt(lastPage); page++) {
            parse(username, page);
        }
        
    } catch (error) {
        console.log('error', error);
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
        console.log(error);
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
            const href = 'http://www.filmow.com' + movie.querySelector('.wrapper a.tip-movie').href;
            parseMovie(href, rating);
        });
    } catch (error) {
        console.log(error);
    }
}

const calculateUserRating = (userRating) => {
    if (userRating) {
        const totalRating = userRating.match(/width: (.*?).0%/)[1];
        const ratingOutOf5 = totalRating / 20;
        console.log(ratingOutOf5);
        return ratingOutOf5;
    }
}

const parseMovie = async (href, rating) => {
    try {
        const response = await axios.get(href);
        const {document} = new JSDOM(response.data).window;
        const title = document.querySelector('h2.movie-original-title')
            ? document.querySelector('h2.movie-original-title').innerHTML
            : document.querySelector('h1');
        const directors = document.querySelector('.directors span strong')
            ? document.querySelector('.directors span strong').innerHTML
            : '';
        const year = document.querySelector('small.release')
            ? document.querySelector('small.release').innerHTML
            : '';
        i += 1
        if (i >= 1900) {
            fileNumber += 1;
            i = 0
        }
        writeToCsv([title, directors, year, calculateUserRating(rating)], fileNumber);
    } catch (error) {
        console.log(error);
    }
  }