"use strict";

////// Key document elements //////
const dropDown = document.querySelector('select[name="country-dropdown"]');
const countryCodeSelectButton = document.getElementById("country-code-selector");
const newsDiv = document.querySelector("#news-dashboard");
const dashboard = document.querySelector("#dashboard-parent");
const countryInfoDiv = document.querySelector("#country-info");


/////// HELPER Functions for the Button Event /////////

/** Create and call the REST Countries API */
function restCountriesCall(twoDigCountryCode) {
    const RESTcountiresURL = "https://restcountries.com/v2/alpha/"
    fetch(`${RESTcountiresURL}${twoDigCountryCode}`)
        .then(response => response.json())
        .then(countryData => {
            countryInfoDiv.insertAdjacentHTML('beforeend',
            `<h2>${countryData.name}</h2>
            <img src=${countryData.flag} id="country-flag">
            <p>Capital: ${countryData.capital} |
            Population: ${countryData.population}<br>
            Currency: (${countryData.currencies[0].code}) 
            ${countryData.currencies[0].name} |
            Primary Language: ${countryData.languages[0].name}`)
        })
}
/**Create News API call using country as keyword */
function countryNameNewsAPIcall(twoDigCountryCode) {
    const queryString = new URLSearchParams({twoDigCountryCode}).toString();
    fetch(`/api/news-by-country-name?${queryString}`)
        .then(articles => articles.json())
        .then(articlesJSON =>  { 
            for (const i in articlesJSON) {
                newsDiv.insertAdjacentHTML('beforeend', 
                `<h3>${articlesJSON[i].title}</h3>
                <img src=${articlesJSON[i].urlToImage} id="news-pic"/>
                <p>${articlesJSON[i].description}
                <a href="${articlesJSON[i].url}">Continue reading</a></p>`);
            }
        });        
}


/** Refresh the page so that the blocks are cleared */
function refreshPage() {
    // Clear previous country
    newsDiv.innerHTML = `<h2>In the News</h2>`
    countryInfoDiv.innerHTML = ""
    // display blocks
    dashboard.style.display = "inline-block"
}

/////// MAIN EVENT: Sumbit button event ////////////
countryCodeSelectButton.addEventListener("click", (evt) => {
    evt.preventDefault();
    const twoDigCountryCode = dropDown.value.toLowerCase();

    refreshPage()
    countryNameNewsAPIcall(twoDigCountryCode)

    // REST Countries API call
    restCountriesCall(twoDigCountryCode);

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
