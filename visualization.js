d3.csv("data/t1-s1.csv")
    .row(function(d) {return {key: d.key, value: +d.value}; })
    .get(function(error, rows) {console.log(rows); });