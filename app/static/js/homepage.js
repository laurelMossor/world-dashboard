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


//////////// HELPER Functions for the Button Event ///////////////

// **** I'm going to need to make mutliple fetchs, using name and full name
/** Create and call the REST Countries API */
function restCountriesCall(countryName) {
    // const RESTcountiresURL = "https://restcountries.com/v2/alpha/"
    fetch(`https://restcountries.com/v2/name/${countryName}?fullText=true`)
        // .then(response => console.log(response.url))
        .then(response => response.json())
        .then(countryData => {
            countryInfoDiv.insertAdjacentHTML('beforeend',
            `<h2>${countryData[0].name}</h2>
            <img src=${countryData[0].flag} id="country-flag">
            <p>Capital: ${countryData[0].capital} |
            Population: ${countryData[0].population}<br>
            Currency: (${countryData[0].currencies[0].code}) 
            ${countryData[0].currencies[0].name} |
            Primary Language: ${countryData[0].languages[0].name}`)
        })
}
/**Create News API call using country as keyword */
function countryNameNewsAPIcall(countryName) {
    const queryString = new URLSearchParams({countryName}).toString();
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

function generateDashboard(evt, countryName) {
    evt.preventDefault();
    refreshPage();
    countryNameNewsAPIcall(countryName);
    restCountriesCall(countryName);
};


/** Generate dynamic button for generating dashboard */
// THIS will hold the MAIN EVENT -- 
// Generate button, on click -> generateDashboard
    // prevent default, 
    // refresh page, 
    // get country name, 
    // country name news call
    // rest countries call 

function dynamicButton(evt) {
    // Upon click of a country, button is generated using the evt target
    const countryName = evt.target.id;
    d3.select("#country-name-box-parent")
        .html("")
        .append("form")
        .insert("button")
        .attr("type", "submit")
        .attr("id", "generate-dashboard-button")
        .text(`${countryName}: Generate Dashboard`)
        .on("click", (evt) => generateDashboard(evt, countryName))
};



/////// MAIN EVENT: Sumbit button event ////////////
// New button event will need to be the dynamically generated button
// countryCodeSelectButton.addEventListener("click", (evt) => {
//     evt.preventDefault();
//     const twoDigCountryCode = dropDown.value.toLowerCase();

//     refreshPage()
//     countryNameNewsAPIcall(twoDigCountryCode)

//     // REST Countries API call
//     restCountriesCall(twoDigCountryCode);

// });


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
            .on("click", (evt) => dynamicButton(evt))
            .append("title").text(function(d) {return `${d.properties.NAME}`;})
            ;
        });



// Function, on click -> create a button to generate Dashboard
// d3.select("#country-name-box-parent")

