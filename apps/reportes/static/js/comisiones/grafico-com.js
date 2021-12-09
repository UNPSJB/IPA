//var data_informacion = $.extend(true,[], informacion);

//_.map(data_informacion, function(e){ 
//  e.fecha = e.fecha.replace(/(\d{4})-(\d{2})-(\d{2})/, "$3/$2/$1");})
//let groupedResults = _.groupBy(data_informacion, (d) => moment(d.fecha, 'DD/MM/YYYY').startOf('isoMonth'));



const eliminaDuplicados = (arr) => {
  return arr.filter((valor, indice) => {
    return arr.indexOf(valor) === indice;
  });
}

const data = [{"modDate":"2017-06-20"},{"modDate":"2017-06-25"},{"modDate":"2017-10-24"},{"modDate":"2017-10-20"},{"modDate":"2017-08-03"}];




//https://bramantox.wordpress.com/2019/10/06/how-to-show-values-on-top-of-bars-in-chart-js/
/* var datasets = {
  labels: [],
  datasets: [{
      label: 'Users',
      //backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
      //borderColor: window.chartColors.red,
      borderWidth: 1,
      data: [53,117,79,56,45,89,61]
  }, {
      label: 'My Users',
      //backgroundColor: color(window.chartColors.blue).alpha(0.5).rgbString(),
      //borderColor: window.chartColors.blue,
      borderWidth: 1,
      data: [43,105,76,50,33,97,52]
  }]

}; */




//let grouped_items = _.groupBy(data_informacion, (b) =>
  //moment(b.fecha).startOf('month').format('YYYY/MM'));
/*
let grouped_items = _.groupBy(data_informacion, (b) =>
  moment(b.fecha).startOf('month').format('YYYY/MM'));

_.values(grouped_items)
  .forEach(arr => arr.sort((a, b) => moment(a.fecha).day() - moment(b.fecha).day()));

console.log(grouped_items);

let data3 = [];
for (const p in data_informacion){
    data3.push(_.groupBy(data_informacion[p], (b) => moment(b.fecha).startOf('month').format('YYYY/MM')));
}
*/

$(document).ready(function () {

    $("#item-grafico").on("click",function(){
      $(".secondary.menu a").attr("class","item");
      $(this).attr("class","active item");
      $("form").hide()
      $("#informacion").hide();
      $("#graficos").show();
      
      $("#row-graficos").empty();
  

      var data_informacion = $.extend(true,[], informacion);  //Hago copias de valores



      var tipos_seperados = _.groupBy(data_informacion, function(e){ return e.tipo; }); // separo por comision, acta insp y acta infra
      
      let data2 = [];
      
      for (const [key, value] of Object.entries(tipos_seperados)) {
        data2.push(_.groupBy(value, (b) => moment(b.fecha).startOf('month').format('MM/YYYY')))  // agrupo cada uno de ellos por fechas
      }
      
      
      fechas = []
      for (const f in data2) {
        fechas = fechas.concat(Object.keys(data2[f]))      // Uno todas las fechas que tengo
      }
      
      fechas_no_duplicadas = eliminaDuplicados(fechas)              // Elimino valores duplicados --> van a ser mis labels
      
      tipos_separados_agrup = {}
      
      for (const [key, value] of Object.entries(tipos_seperados)) {
        tipos_separados_agrup[key] = _.groupBy(value, (b) => moment(b.fecha).startOf('month').format('MM/YYYY'))  // agrupo cada uno de ellos por fechas
      }
      
      var datasets_final = {"comision": {},'acta-de-inspeccion':{},'acta-de-infraccion':{}}
      var datasets_cantidades = {"comision": [],'acta-de-inspeccion':[],'acta-de-infraccion':[]}
      for(let ts in tipos_separados_agrup){
        for (let f in fechas_no_duplicadas.reverse()){
          if (tipos_separados_agrup[ts][fechas_no_duplicadas[f]] !== undefined){
            datasets_final[ts][fechas_no_duplicadas[f]] = Object.keys(tipos_separados_agrup[ts][fechas_no_duplicadas[f]]).length
            datasets_cantidades[ts].push(Object.keys(tipos_separados_agrup[ts][fechas_no_duplicadas[f]]).length)
          }else{
            datasets_final[ts][fechas_no_duplicadas[f]] = 0
            datasets_cantidades[ts].push(0)
          }
        }
      }

    var datasets = {
        labels: fechas_no_duplicadas,
        datasets: [{
            label: 'Comision',
            backgroundColor: '#DE7B66',
            borderColor: '#DE7B66',
            borderWidth: 1,
            data: datasets_cantidades['comision']
        }, {
            label: 'A. Inspección',
            backgroundColor: '#DAD527',
            borderColor: '#DAD527',
            borderWidth: 1,
            data: datasets_cantidades['acta-de-inspeccion']
        },{
          label: 'A. Infracción',
          backgroundColor: '#3FEF3D',
          borderColor: '#3FEF3D',
          borderWidth: 1,
          data: datasets_cantidades['acta-de-infraccion']
      }]
    
    };
  
      $("#row-graficos").append('<canvas id="line-chart">');
      grafico = new Chart($("#line-chart"), {
        type: 'bar',
        data: datasets,
        options: {
            responsive: true,
            "hover": {
              "animationDuration": 0
            },
            "animation": {
                "duration": 1,
            },
            scales: {
              yAxes: {
                title: {
                  display: true,
                  text: 'Cantidad'
                },
                ticks: {
                  min: 0,
                  stepSize: 1,
                },
              },
              xAxes: {
                  title: {
                    display: true,
                    text: 'Mes/Año'
                  }
              }
            },
            plugins: {
              title: {
                  display: true,
                  text: 'Comisiones vs Actas de Inspección vs Actas de Infracción',
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
      }
    );
  });
});