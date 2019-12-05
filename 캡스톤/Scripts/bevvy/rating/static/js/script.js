$(function() {
    $("ul.chart").hBarChart({});
    $("ul.chart1").hBarChart({
        bgColor: '#C000',
        textColor: '#fff',
        sorting: true,
        maxStyle: {
            bg: 'orange',
            text: 'white'
        }
    });
})