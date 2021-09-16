var label_canon = [];
var data_canon = [];

$("#item-info-grafico").on("click",function(){
    $("form").hide()
    $(".secondary.menu a").attr("class","item");
    $(this).attr("class","active item");
});

function getDataLabel(motivo,operacion){
    let labels = [];
    let data = []
    for (let i of Object.keys(informacion).slice(0,-1)){
        if(motivo in informacion[i] && operacion in informacion[i][motivo]){
            data.push(informacion[i][motivo][operacion])
        }
        labels.push(i);
    }
    return [data,labels];
}


$("#item-grafico").on("click",function(){
    $(".secondary.menu a").attr("class","item");
    $(this).attr("class","active item");
    $("form").hide()
    $("#informacion").hide();
    $("#graficos").show();
    
    $("#row-graficos").empty();

    if (typeof informacion !== 'undefined'){
        var motivos = tabla_head_rw1_th[dataset["motivos"]];
        var operaciones = tabla_head_rw2_th[dataset["operaciones"]];
        if (operaciones.length==3)
            operaciones.pop();
    
        for (let m of motivos){
            for (let o of operaciones){
                [data_canon,label_canon] = getDataLabel(m,o);
                $("#row-graficos").append('<div style=width: 35%;><canvas id='+m+'-'+o+'-pie-chart></div>');
                var c = new Chart($("#"+m+"-"+o+"-pie-chart"), {
                    type: 'bar',
                    data: {
                        labels: label_canon,
                        datasets: [{
                            label: m +' - '+o,
                            data: data_canon,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
        }    
    }

});
