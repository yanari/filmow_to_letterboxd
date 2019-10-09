const request = require('request');
const axios = require('axios');
const jsdom = require('jsdom');

const {writeToCsv} = require('./writer');

const {JSDOM} = jsdom;

let i = 0;
let fileNumber = 1;

module.exports.getLastPage = (username, cb) => {
  request(`https://filmow.com/usuario/${username}/filmes/ja-vi/`, (err, res, body) => {
    if (res && res.statusCode === 200 && !err) {
      const {document} = new JSDOM(body).window;
      const pages = document.querySelectorAll('.pagination ul li a');
      const lastPageHref = pages[pages.length - 1].href;
      const lastPage = lastPageHref.match(/pagina=(\w+)/)[1];
      for (let page = 1; page <= lastPage; page++) {
        parse(username, page, cb)
      }
    }
  });
}

const parse = (username, page, cb) => {
  request(`https://filmow.com/usuario/${username}/filmes/ja-vi?pagina=${page}`, (err, res, body) => {
    if (res && res.statusCode === 200 && !err) {
      const {document} = new JSDOM(body).window;
      const movies = document.querySelectorAll('li.movie_list_item');
      movies.forEach(movie => {
        const userRatingSelector = movie.querySelector('.user-rating .average');
        const userRating = userRatingSelector ? userRatingSelector.getAttribute('style') : null;
        calculateUserRating(userRating);
        const href = 'http://www.filmow.com' + movie.querySelector('.wrapper a.tip-movie').href;
        parseMovie(href, userRating, cb);
      });
    }
  });
}

const parseMovie = (href, rating, cb) => {
  request(href, (err, res, body) => {
    if (res && res.statusCode === 200 && !err) {
      const {document} = new JSDOM(body).window;
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
      cb(title, directors, year, calculateUserRating(rating))
    }
  });
}

const calculateUserRating = (userRating) => {
  if (userRating) {
    const totalRating = userRating.match(/width: (.*?).0%/)[1];
    const ratingOutOf5 = totalRating / 20;
    return ratingOutOf5;
  }
}
