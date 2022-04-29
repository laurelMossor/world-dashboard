"use strict";


// "/static/map-files/world-map-Geo.geojson"
// "/static/map-files/map-topojson-LITE.json"
// static/map-files/world-map-TOPO.json


// let width = 850;
// let height = 520;

// const projection = d3.geoMercator()
//     .center([0, 20])
//     .scale(120)
//     .rotate([-10,0]);

// const svg = d3.select("#clickable-map");
//     svg.attr("width", width);
//     svg.attr("height", height);

// const path = d3.geoPath()
//     .projection(projection);

// const g = svg.append("g");

// // load and display the World
// d3.json("static/map-files/world-map-TOPO.json")
//     .then(function(topology) {
//         g.selectAll("path")
//             .data(topojson.feature(topology, topology.objects.ne_10m_admin_0_sovereignty).features)
//             .enter().append("path")
//             .attr("d", path)
//             .attr("fill", "grey")
//             .attr("stroke", "white")
//             .attr("stroke-width", "0.5px");
            
//         }

// )
// // event listeners here?
// ;

// PLAYING AROUND!!!

let width = 600;
let height = 400;
// let myMap = new Map()

const projection = d3.geoMercator()
    .center([0, 20])
    .scale(100)
    // .rotate([-10,0])
    .translate([width / 2, height / 2]);
    
const path = d3.geoPath()
.projection(projection);
    
const svg = d3.select("#clickable-map");
    svg.attr("width", width);
    svg.attr("height", height);


const g = svg.append("g");

// load and display the World
d3.json("/static/map-files/world-map-Geo.geojson")
    .then(function(geoJSONdata) {
        g.selectAll("path")
            .data(geoJSONdata.features)
            .enter()
            .append("path")
            // Draw each country
            .attr("d", path)
            .attr("fill", "transparent")
            .attr("stroke", "black")
            .attr("stroke-width", "0.25px")
            .attr("name", (d) => {d.properties.NAME})
            .attr("class", "Country")
            .attr("name", (d, i) => {i});
            // .on("click", (evt) => {
            //     let x = d3.selectAll(".Country")
            //     console.log(x._groups[0]);
            // });
            
        
            
        }

)
;
// const allCountriesClass = d3.selectAll(".Country")

// for (const country of allCountriesClass){

//     country.addEventListener("click" , (evt) =>{
//         evt.preventDefault();

//         console.log(evt.target);
//     })
// };
// console.log(d3.map["US"])


