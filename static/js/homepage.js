"use strict";

/** This visualization was made possible by utilizing and altering code from the following examples:
    * Choropleth map with hover effect in d3.js by Yan Holtz from: 
        * https://d3-graph-gallery.com/graph/choropleth_hover_effect.html
    * World Map Centered v7 by d3noob, released under the MIT license from:
        *  https://bl.ocks.org/d3noob/82f4db23d47971c74699abb5f4bf8204
 */


////////////////// Key document elements /////////////
const dropDown = document.querySelector('select[name="country-dropdown"]');
const countryCodeSelectButton = document.getElementById("country-code-selector");
const newsDiv = document.querySelector("#news-dashboard");
const dashboard = document.querySelector("#dashboard-parent");
const countryInfoDiv = document.querySelector("#country-info");


//////////// HELPER Functions for the Button Event ///////////////

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


//////////////////////////// Map specs /////////////////////////
let width = 850;
let height = 520;

const projection = d3.geoMercator()
    .center([0, 20])
    .scale(120)
    .rotate([-10,0]);

const svg = d3.select("#clickable-map");
    svg.attr("width", width);
    svg.attr("height", height);
    svg.attr("viewBox", [0,0,width,height]);

const path = d3.geoPath()
    .projection(projection);

const g = svg.append("g");

/////// Zoom function ////////
svg.call(d3.zoom()
    .extent([[0,0], [width, height]])
    .scaleExtent([1,8])
    .on("zoom", (event) => {
        g.attr("transform", event.transform);
}
));

//////////////////////////// Load and display the World /////////////////////
d3.json("static/map-files/world-map-TOPO.json")
    .then(function(data) {
        const sovreignCountries = topojson.feature(data, data.objects.ne_10m_admin_0_sovereignty);
        g.selectAll("path")
            .data(sovreignCountries.features)
            .enter().append("path")
            .attr("d", path)
            .attr("class", "Country")
            .attr("id", function(d) {
            return `${d.properties.NAME}`
            })
            .on("click", function(evt) {
                // evt.target.id is the country name, and that's how we'll call the APIs
                // I want a box to show up with a tooltip:
                    // Displays country name, and a button that says "Activate Dashboard"
                const countryName = evt.target.id;
                d3.select("#country-name-box").text(`${countryName}`);

            })
            .append("title").text(function(d) {return `${d.properties.NAME}`;})
            ;
        });

