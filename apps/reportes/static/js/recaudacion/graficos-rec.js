var label_canon = [];
var data_canon = [];

var grafico;

function getDataLabel(motivo,operacion){
    let labels = [];
    let data = [];
    for (let i of Object.keys(informacion).slice(0,-1)){
        if(motivo in informacion[i] && operacion in informacion[i][motivo]){
            data.push(informacion[i][motivo][operacion])
        }
        labels.push(i);
    }
    return [data,labels];
}

function graficos_tipos_permisos(){
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
}

const randomNum = () => Math.floor(Math.random() * 255);

const randomRGB = (mot) => {
    if(mot=="Cobro"){
        return 'rgb(255, 0, 0)';
    }else{
        return `rgb(0, 143, 57)`;
    }
}

function graficos_series_temporales(){
    var timeFormat = 'DD/MM/YYYY';
    var data_informacion = $.extend(true,[], informacion);

    _.map(data_informacion, function(e){ 
        e.fecha = new Date(e.fecha.replace(/(\d{4})-(\d{2})-(\d{2})/, "$2/$3/$1"));
        e.motivo ? e.motivo= "Canon" : e.motivo= "Infraccion"});

    if (typeof informacion !== 'undefined'){
        datasets = []

        datos = _.groupBy(_.sortBy(data_informacion, "fecha"), "operacion");
        datos_nombres = Object.getOwnPropertyNames(datos).sort().reverse();
        
        
        var acum_cobro = 0;
        var acum_pago = 0;
        Object.entries(datos).forEach(([motivo, movimiento]) => {
            console.log("clave:" + motivo); // "a 5", "b 7", "c 9"
            movimiento.forEach(e => {
                if (e.operacion=="Cobro"){
                    acum_cobro+=e.monto
                    e.monto = acum_cobro
                }else{
                    acum_pago+=e.monto
                    e.monto = acum_pago
                }
                console.log(e)
            })
        });        

        for (const o in datos_nombres) {
            datasets.push({
                label:datos_nombres[o],
                data: datos[datos_nombres[o]],
                borderColor: randomRGB(datos_nombres[o])
            })
        }

    $("#row-graficos").append('<canvas id="line-chart">');
    grafico = new Chart($("#line-chart"), {
        type: 'line',
        data: {
            datasets:datasets
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Recaudación - Serie de Tiempo',
                    padding: {
                        top: 10,
                        bottom: 10
                    },
                    font:{
                        size:30
                    }
                }
            },
            scales:{
                xAxes:{
                    title:{
                        display: true,
                        text: 'Tiempo',
                        font:{
                            size:20
                        }
                    },
                    type:'time',
                    time:{
                        format: timeFormat,
                        unit:'day',
                        stepSize: 10,
                        tooltipFormat:'DD/MM/YYYY',
                        displayFormats:{
                            day:'DD/MM/YYYY',
                            month:'MM/YYYY',
                            year:'YYYY',
                            quarter: 'MMM/YYYY'
                        }
                        
                    }
                },
                yAxes: {
                    title:{
                        display: true,
                        text: 'Monto',
                        font:{
                            size:20
                        }
                    },
                    ticks: {
                        callback: function(value, index, values) {
                            return '$' + value;
                        }
                    },
                    beginAtZero: false
                }
            },
            parsing: {
                xAxisKey: 'fecha',
                yAxisKey: 'monto'
            }
        }
    });
    }

}



function graficos_proyeccion_vm (){

    var data_informacion = $.extend(true,[], informacion);

    datos = _.groupBy(_.sortBy(data_informacion, "fecha"), "tipo");

    var datasets_final = {}
    for (let t of Object.keys(datos)){
        datasets_final[t] = 0
    }

    for (const [key, value] of Object.entries(datos)) {
            value.forEach(e => 
                datasets_final[key] += datasets_final[key]+parseFloat(e.monto.replace(",", "."))
            )
      }


    $("#row-graficos").append('<canvas id="line-chart">');
    grafico = new Chart($("#line-chart"), {
        type: 'pie',
        data: {
        labels: Object.keys(datasets_final),
            datasets: [{
                label: "Population (millions)",
                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                data: Object.values(datasets_final)
            }]
        },
        options: {
            responsive: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Proyección de Ingresos por Tipo de Permiso',
                    padding: {
                        top: 10,
                        bottom: 10
                    },
                    font:{
                        size:30
                    }
                }
            },
        }
    });

}


$("#item-grafico").on("click",function(){
    $(".secondary.menu a").attr("class","item");
    $(this).attr("class","active item");
    $("form").hide()
    $("#informacion").hide();
    $("#graficos").show();
    
    $("#row-graficos").empty();
   
    switch (dataset['tipo_reporte']) {
        case "tipos_permisos": graficos_tipos_permisos(); break;
        case "series_temporales": graficos_series_temporales(); break;
        case "proyeccion_valores_modulos": graficos_proyeccion_vm(); break;
    }  

});
