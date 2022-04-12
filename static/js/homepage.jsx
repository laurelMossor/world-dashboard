"use strict";

// News API accepted country codes
const COUNTRY_CODES = ['ae', 'ar', 'at', 'au', 'be', 'bg', 
'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 
'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 
'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 
'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 
'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 
'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'];

// 2-digit country code selection
const countryCodeSelectButton = document.getElementById("country-code-selector");
const newsDiv = document.querySelector("#news-dashboard")
const dashboard = document.querySelector("#dashboard-parent")

// News API call

countryCodeSelectButton.addEventListener("click", (evt) => {
    evt.preventDefault();
    const twoDigCountryCode = document.querySelector('select[name="country-code-select"]').value;
    const queryString = new URLSearchParams({twoDigCountryCode}).toString();
    newsDiv.innerHTML = ""
    dashboard.style.display = "inline-block"

    fetch(`/news-country?${queryString}`)
        .then(articles => articles.json())
        .then(articlesJSON =>  {


            for (const i in articlesJSON) {
                newsDiv.insertAdjacentHTML('beforeend', 
                `<h3>${articlesJSON[i].title}</h3>
                <img src=${articlesJSON[i].urlToImage} id="news-pic"/>
                <p>${articlesJSON[i].content}</p>`);
            }
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
