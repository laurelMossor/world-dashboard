"use strict";
// import { select, json } from 'd3';


    // width = +mapSVG.attr("width"),
    // height = +mapSVG.attr("height");





fetch("/static/map-files/world-map-Geo.geojson")
    .then(mapData => mapData.json())
    .then(responseData => {

        // svg
        let mapSVG = d3.select("svg");
        let width = mapSVG.attr("width");
        let height = mapSVG.attr("height");

        // Map and projection
        let projection = d3.geoNaturalEarth1()
        .scale(width / 1.3 / Math.PI)
        .translate([width / 2, height / 2])

        // Everything goes here
        // Instead of the url, give it d3.json(responseData)
        d3.json(responseData, function(data){

                // Draw the map
            mapSVG.append("g")
                .selectAll("path")
                .data(data.features)
                // Features is how it draws the lines
                .enter().append("path")
                    .attr("fill", "#69b3a2")
                    .attr("d", d3.geoPath()
                        .projection(projection)
                    )
                    .style("stroke", "#fff")
        })
    })




