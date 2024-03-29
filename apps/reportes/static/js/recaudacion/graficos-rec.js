var label_canon = [];
var data_canon = [];
var datasets_final = {}
var monto_total = 0;
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
    $("#graficos").empty();
    if (typeof informacion !== 'undefined'){
        var cobro_canon = []
        var pago_canon = []
        var cobro_infraccion = []
        var pago_infraccion = []
        labels_permisos = Object.keys(informacion).slice(0,-1) //SACAR TOTALES
        
        for (var [key, value] of Object.entries(informacion)) { // Tipos de Permisos
            if(key!="TOTALES"){
                for (var [key2, value2] of Object.entries(value)) { // Canon e Infraccion
                    for (var [key3, value3] of Object.entries(value2)) { // Pago y Cobro
                        if(key3 != "Diferencia"){
                            if (key2 == "Canon"){
                                if(key3 == "Cobro"){
                                    cobro_canon.push(value3);
                                }else{
                                    pago_canon.push(value3);
                                }
                            }else{
                                if(key3 == "Cobro"){
                                    cobro_infraccion.push(value3);
                                }else{
                                    pago_infraccion.push(value3);
                                }
                            }
                        }
                    }
                }
            }
        }
        
        var datasetsff = {
            labels: labels_permisos,
            datasets: [{
                label: 'Cobro',
                backgroundColor: '#DE7B66',
                borderColor: '#DE7B66',
                borderWidth: 1,
                data: cobro_canon
            }, {
                label: 'Pago',
                backgroundColor: '#DAD527',
                borderColor: '#DAD527',
                borderWidth: 1,
                data: pago_canon
            }]
        };
        
        $("#graficos").append('<canvas id="line-chart">');
        grafico = new Chart($("#line-chart"), {
            type: 'bar',
            data: datasetsff,  
            options: {
                responsive: true,
                scales: {
                    yAxes: {
                        title: {
                            display: true,
                            text: 'Montos ($)'
                        },
                    },
                    xAxes: {
                        title: {
                        display: true,
                        text: 'Tipos de Permiso'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Cobro vs Pagos - Canon',
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

         var datasetszz = {
            labels: labels_permisos,
            datasets: [{
                label: 'Cobro',
                backgroundColor: '#DE7B66',
                borderColor: '#DE7B66',
                borderWidth: 1,
                data: cobro_infraccion
            }, {
                label: 'Pago',
                backgroundColor: '#DAD527',
                borderColor: '#DAD527',
                borderWidth: 1,
                data: pago_infraccion
            }]
        };
        
        $("#graficos").append('<canvas id="chart2">');
        grafico2 = new Chart($("#chart2"), {
            type: 'bar',
            data: datasetszz,
               
            options: {
                responsive: true,
                scales: {
                    yAxes: {
                        title: {
                            display: true,
                            text: 'Montos ($)'
                        },
                    },
                    xAxes: {
                        title: {
                        display: true,
                        text: 'Tipos de Permiso'
                        }
                    }
                },
            
                plugins: {
                    title: {
                        display: true,
                        text: 'Cobro vs Pagos - Infracciones',
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
};         


const randomNum = () => Math.floor(Math.random() * 255);

const randomRGB = (mot) => {
    if(mot=="Cobro"){
        return 'rgb(255, 0, 0)';
    }else{
        return `rgb(0, 143, 57)`;
    }
}

function graficos_series_temporales(){
    $("#graficos").empty();

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
            movimiento.forEach(e => {
                if (e.operacion=="Cobro"){
                    acum_cobro+=e.monto
                    e.monto = acum_cobro
                }else{
                    acum_pago+=e.monto
                    e.monto = acum_pago
                }
            })
        });        

        for (const o in datos_nombres) {
            datasets.push({
                label:datos_nombres[o],
                data: datos[datos_nombres[o]],
                borderColor: randomRGB(datos_nombres[o])
            })
        }

    $("#graficos").append('<canvas id="chart3">');
    grafico3 = new Chart($("#chart3"), {
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


function toPercent(num){
	var porcentaje = Number(num*100).toFixed(2);
    porcentaje+="%";
	return porcentaje;
}

function graficos_proyeccion_vm (){
    $("#graficos").empty();

    var data_informacion = $.extend(true,[], informacion);

    datos = _.groupBy(_.sortBy(data_informacion, "fecha"), "tipo");

    datasets_final = {}
    monto_total = 0;

    for (let t of Object.keys(datos)){
        datasets_final[t] = 0
    }

    for (const [key, value] of Object.entries(datos)) {
            value.forEach(e => {
                datasets_final[key] += parseFloat(e.monto.replace(".", ","));
                monto_total += parseFloat(e.monto.replace(",", "."));
                })
      }

    $("#graficos").append("<div class='chart-container' style='position: relative; height:20vh; width:40vw'><canvas id='chart4'></div>");
    
    grafico4 = new Chart($("#chart4"), {
        type: 'pie',
        data: {
        labels: Object.keys(datasets_final),
            datasets: [{
                //label: "Population (millions)",
                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#F45850","#c4FF50","#A45B50","#DD1850","#c4CC50","#c4BA50","#AA58CC","#c45ABC","#DD812F"],
                data: Object.values(datasets_final)
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: "Reporte de Recaudación - Proyección por Valor de Módulo - Grafico",
                    padding: {
                        top: 10,
                        bottom: 10
                    },
                    font:{
                        size:30
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label+": ";                            
                            label += toPercent(datasets_final[context.label]/monto_total);
                            return label;
                        }
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
    
    $("#graficos").empty();
   
    switch (dataset['tipo_reporte']) {
        case "tipos_permisos": graficos_tipos_permisos(); break;
        case "series_temporales": graficos_series_temporales(); break;
        case "proyeccion_valores_modulos": graficos_proyeccion_vm(); break;
    }  

});
