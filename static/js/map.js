"use strict";



// "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"
// "/static/map-files/world-map-Geo.geojsonj"





        let width = 960;
        let height = 500;

        const projection = d3.geoMercator()
        .center([0, 5 ])
        .scale(150)
        .rotate([-180,0]);

        const svg = d3.select("#clickable-map");
            svg.attr("width", width);
            svg.attr("height", height);

        const path = d3.geoPath()
            .projection(projection);

        const g = svg.append("g");

// load and display the World
        d3.json("/static/map-files/map-topojson-LITE.json").then(function(topology) {

            g.selectAll("path")
            .data(topojson.feature(topology, topology.objects.ne_10m_admin_0_countries).features)
            .enter().append("path")
            .attr("d", path);

        })
        // event listeners here?
        ;




