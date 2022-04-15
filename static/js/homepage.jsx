"use strict";

// News API accepted country codes
const COUNTRY_CODES = ['ae', 'ar', 'at', 'au', 'be', 'bg', 
'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 
'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 
'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 
'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 
'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 
'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'];

const COUNTRY_CODES_WIP = [("ae", "United Arab Emirates"), 
("ar", "Argentina"), ("at", "Austria")]



// const svgMap = Object({
//     targetElementID: 'svgMapExample',
// });
// new svgMap({
//     targetElementID: 'svgMapExample',
// });



// Countries Info 
const RESTcountiresURL = "https://restcountries.com/v2/alpha/"

// Creating form on JS side
const dropDown = document.querySelector('select[name="country-code-select"]');
for (const code of COUNTRY_CODES) {
    dropDown.insertAdjacentHTML('beforeend',
    `<option value=${code}>${code}</option>`)
};

// Key document elements
const countryCodeSelectButton = document.getElementById("country-code-selector");
const newsDiv = document.querySelector("#news-dashboard");
const dashboard = document.querySelector("#dashboard-parent");
const countryInfoDiv = document.querySelector("#country-info");

// Sumbit button event
countryCodeSelectButton.addEventListener("click", (evt) => {
    evt.preventDefault();
    const twoDigCountryCode = document.querySelector('select[name="country-code-select"]').value;
    const queryString = new URLSearchParams({twoDigCountryCode}).toString();
    // Clear previous country
    newsDiv.innerHTML = `<h2>TOP NEWS</h2>`
    countryInfoDiv.innerHTML = ""

    // display blocks
    dashboard.style.display = "inline-block"

    // News API call
    fetch(`/news-country?${queryString}`)
        .then(articles => articles.json())
        .then(articlesJSON =>  {

            for (const i in articlesJSON) {
                newsDiv.insertAdjacentHTML('beforeend', 
                `<h3>${articlesJSON[i].title}</h3>
                <img src=${articlesJSON[i].urlToImage} id="news-pic"/>
                <p>${articlesJSON[i].content}</p>`);
            }
        });
    // REST Countries API call
    fetch(`${RESTcountiresURL}${twoDigCountryCode}`)
        .then(response => response.json())
        .then(countryData => {
            console.log(countryData.currencies);
            countryInfoDiv.insertAdjacentHTML('beforeend',
            `<h2>${countryData.name}</h2>
            <img src=${countryData.flag} id="country-flag">
            <p>Capital: ${countryData.capital} |
            Population: ${countryData.population} |
            Currency: (${countryData.currencies[0].code}) ${countryData.currencies[0].name}`)
        })

});



// function RenderNews() {
//     // Country code choice as state?
//     const [news, showNews] = React.useState([]);

//     React.useEffect(() => {
//         fetch("/news-country-test")
//             .then((response) => response.json())
//             .then((result) => {
//                 showNews(result);
//             });
//     }, []);

//     const newsList = [news];

//     return <p>{newsList}</p>
// }


// ReactDOM.render(<RenderNews />, 
// document.querySelector('#news-dashboard'));

// Practice just by rendering the country code at the bottom
