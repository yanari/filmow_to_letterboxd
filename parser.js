const axios = require('axios').default;
const jsdom = require('jsdom');

const {JSDOM} = jsdom;

module.exports.parsePage = async (username) => {
    try {
        const lastPage = await getLastPage(username);
        console.log(lastPage);
        
    } catch (error) {
        console.log(error);
    }
}

const getLastPage = async (username) => {
    const response = await axios.get(`https://filmow.com/usuario/${username}/filmes/ja-vi/`);
    const { document } = new JSDOM(response.data).window;
    const pages = document.querySelectorAll('.pagination ul li a');
    const lastPageHref = pages[pages.length - 1].href;
    return lastPageHref.match(/pagina=(\w+)/)[1];
}
