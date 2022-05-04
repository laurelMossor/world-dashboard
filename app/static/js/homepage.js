"use strict";

/** This visualization was made possible by utilizing and altering code from the following examples:
    * Choropleth map with hover effect in d3.js by Yan Holtz from: 
        * https://d3-graph-gallery.com/graph/choropleth_hover_effect.html
    * World Map Centered v7 by d3noob, released under the MIT license from:
        *  https://bl.ocks.org/d3noob/82f4db23d47971c74699abb5f4bf8204
 */


////////////////// Key document elements /////////////
const newsDiv = document.querySelector("#news-dashboard");
const dashboard = document.querySelector("#dashboard-parent");
const countryInfoDiv = document.querySelector("#country-info");
const exchangeRateDiv = document.querySelector("#exchange-rate");


//////////// HELPER Functions for the Button Event ///////////////

/** Async fetch REST API so that I can get the currency code */
async function restCountriesAndExchangeCall(countryCode) {
    // HELPER FUNCTION:  ****generateDashboard(evt, countryName, countryCode)****

    const RESTcountiresURL = "https://restcountries.com/v2/alpha/"
    let response = await fetch(`${RESTcountiresURL}${countryCode}`);
    let countryData = await response.json();
    writeRestCountriesDiv(countryData);

    // Exchange rate API call relies on the currencyCode
    // Must call here
    let currencyCode = await countryData.currencies[0].code;
    exchangeRateAPI(currencyCode)
}

/** Nested function within REST countries to get exchange rate */
function exchangeRateAPI(currencyCode) {
    // HELPER FUNCTION: ****restCountriesAndExchangeCall()****

    const queryString = new URLSearchParams({currencyCode}).toString();
    fetch(`/api/exchange-rate?${queryString}`)
        .then(response => response.json())
        .then(responseJson => writeExchangeRate(responseJson))
}

function writeExchangeRate(responseJson) {
    // HELPER FUNCTION: ****exchangeRateAPI(currencyCode)****

    exchangeRateDiv.insertAdjacentHTML("beforeend",
        `<p>${responseJson["result"]}</p>`
    )
}

/** A split version of pervious function, just write the REST Countries info div */
function writeRestCountriesDiv(countryData) {
    // HELPER FUNCTION: ****restCountriesAndExchangeCall()****
    
    countryInfoDiv.insertAdjacentHTML('beforeend',
            `<h2>${countryData.name}</h2>
            <img src=${countryData.flag} id="country-flag">
            <p><b>Capital</b>: ${countryData.capital} |
            <b>Population</b>: ${countryData.population}<br>
            <b>Currency</b>: ${countryData.currencies[0].name} 
            (${countryData.currencies[0].code}) |
            <b>Primary Language</b>: ${countryData.languages[0].name}`)
}


/**Create News API call using country as keyword */
function countryNameNewsAPIcall(countryName) {
    // HELPER FUNCTION:  ****generateDashboard(evt, countryName, countryCode)****

    const queryString = new URLSearchParams({countryName}).toString();
    fetch(`/api/news-by-country-name?${queryString}`)
        .then(articles => articles.json())
        .then(articlesJSON =>  { 
            for (const i in articlesJSON) {
                newsDiv.insertAdjacentHTML('beforeend', 
                `<h4>${articlesJSON[i].title}</h4>
                <img src=${articlesJSON[i].urlToImage} id="news-pic"/>
                <p>${articlesJSON[i].description}
                <a href="${articlesJSON[i].url}">Continue reading</a></p>`);
            }
        });        
}

/** Refresh the page so that the blocks are cleared */
function refreshPage() {
    // HELPER FUNCTION:  ****generateDashboard(evt, countryName, countryCode)****

    // Clear previous country
    newsDiv.innerHTML = `<h2>In the News</h2>`
    countryInfoDiv.innerHTML = ""
    exchangeRateDiv.innerHTML = ""
    // display blocks
    dashboard.style.display = "inline-block"
}


/////////////////// MAIN EVENT: Sumbit button event ////////////////////
function generateDashboard(evt, countryName, countryCode) {
    // HELPER FUNCTION:  ****dynamicButton(evt)****

    evt.preventDefault();

    // Clear previous results
    refreshPage();

    // Call the News API
    countryNameNewsAPIcall(countryName);

    // REST Countries API call and Exchange Rate call
    restCountriesAndExchangeCall(countryCode);


};

/** Generate dynamic button for generating dashboard */
function dynamicButton(evt) {
    // HELPER FUNCTION:  ****Create Map****

    // Upon click of a country, button is generated using the evt target
    const countryCode = evt.target.id;
    const countryName = document.querySelector(`[id="${countryCode}"] title`).textContent

    d3.select("#country-name-box-parent")
        .html("")
        .append("form")
        .insert("button")
        .attr("type", "submit")
        .attr("class", "text-nowrap btn btn-secondary btn-lg")
        .attr("id", "generate-dashboard-button")
        .attr("data-toggle", "modal")
        .attr("data-target", "#modal-dashboard")
        .text(`${countryName}: Generate Dashboard`)
        .on("click", (evt) => generateDashboard(evt, countryName, countryCode))
};



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
    svg.attr("viewBox", [3,3,width,height]);

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
            .attr("id", function(d) {return `${d.properties.ISO_A2}`})
            .attr("name", function(d) {return `${d.properties.ISO_A2}`})
            .on("click", function(evt) {return dynamicButton(evt);})
            .append("title").text(function(d) {return `${d.properties.NAME}`;})
            ;
        });



// Function, on click -> create a button to generate Dashboard
// d3.select("#country-name-box-parent")

