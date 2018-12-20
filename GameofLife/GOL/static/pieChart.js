
    {/* // var my_js_data = JSON.parse('{"field1": "string value", "field2": 100}'); */}
let chart = new CanvasJS.Chart("chartContainer",
{
    legend: {
        maxWidth: 350,
        itemWidth: 120
    },
    data: [
    {
        type: "pie",    
        legendText: "{indexLabel}",
        dataPoints: [
            { y: st, indexLabel: "Sức khỏe" },
            { y: knl, indexLabel: "Trí tuệ" },
            { y: cre, indexLabel: "Sáng tạo" },
            { y: per, indexLabel: "Nhân phẩm"},
            { y: soc, indexLabel: "Xã hội" }
        ]
    }
    ]
});
chart.render();