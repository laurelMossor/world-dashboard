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
let twoDigCountryCode = document.querySelector('select[name="country-code-select"]').value;
const countryCodeSelectButton = document.getElementById("country-code-selector");
const newsDiv = document.querySelector("#news-dashboard")

// News API call

countryCodeSelectButton.addEventListener("click", (evt) => {
    evt.preventDefault();
    const queryString = new URLSearchParams({twoDigCountryCode}).toString();


    fetch(`/news-country-test?${queryString}`)
        .then(response => response.json())
        .then(responseJson =>  {
            console.log(responseJson);
            for (const article in responseJson) {
                newsDiv.innerHTML = `<p>${article}</p>`;
            }
        })

});
// On submit, Get the country code value,
// send it over to .py,
// .py makes the API call,
// returns tje JSON, 



// const newsApiURL = "https://newsapi.org/v2/top-headlines?"
// const news_payload = {
//     "apikey": myNEWS_API_KEY, 
//     "country": twoDigCountryCode,
//     "pageSize": "5",
// };
// const queryString = new URLSearchParams(news_payload).toString();
// const newsApiCallURL = `${newsApiURL}${queryString}`;
// console.log(newsApiCallURL);


// fetch(newsApiCallURL)
//     .then(response => response.json())
//     .then(responseJson => console.log(responseJson));




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
