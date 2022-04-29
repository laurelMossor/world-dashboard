"use strict";

/** This visualization was made possible by utilizing and altering code from the following examples:
    * Choropleth map with hover effect in d3.js by Yan Holtz from: 
        * https://d3-graph-gallery.com/graph/choropleth_hover_effect.html
    * World Map Centered v7 by d3noob, released under the MIT license from:
        *  https://bl.ocks.org/d3noob/82f4db23d47971c74699abb5f4bf8204
 */


// "/static/map-files/world-map-Geo.geojson"
// "/static/map-files/map-topojson-LITE.json"
// static/map-files/world-map-TOPO.json


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

svg.call(d3.zoom()
    .extent([[0,0], [width, height]])
    .scaleExtent([1,8])
    .on("zoom", (event) => {
        g.attr("transform", event.transform);
}
));

const path = d3.geoPath()
    .projection(projection);

const g = svg.append("g");

// load and display the World
d3.json("static/map-files/world-map-TOPO.json")
    .then(function(data) {
        const countries = topojson.feature(data, data.objects.ne_10m_admin_0_sovereignty);
        g.selectAll("path")
            .data(countries.features)
            .enter().append("path")
            .attr("d", path)
            .attr("class", "Country")
            .append("title").text(function(d) {return `${d.properties.NAME}`;})
        });


let allCountries = d3.selectAll(".Country")




