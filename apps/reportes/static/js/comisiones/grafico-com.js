//var data_informacion = $.extend(true,[], informacion);

//_.map(data_informacion, function(e){ 
//  e.fecha = e.fecha.replace(/(\d{4})-(\d{2})-(\d{2})/, "$3/$2/$1");})
//let groupedResults = _.groupBy(data_informacion, (d) => moment(d.fecha, 'DD/MM/YYYY').startOf('isoMonth'));

const data = [{"modDate":"2017-06-20"},{"modDate":"2017-06-25"},{"modDate":"2017-10-24"},{"modDate":"2017-10-20"},{"modDate":"2017-08-03"}];

var data_informacion = $.extend(true,[], informacion);  //Hago copias de valores

var tipos_seperados = _.groupBy(data_informacion, function(e){ return e.tipo; }); // separo por comision, acta insp y acta infra

let data = []

for (const [key, value] of Object.entries(tipos_seperados)) {
  data.push(_.groupBy(value, (b) => moment(b.fecha).startOf('month').format('YYYY/MM')))  // agrupo cada uno de ellos por fechas
}


fechas = []
for (const f in data) {
  fechas = fechas.concat(Object.keys(data[f]))      // Uno todas las fechas que tengo
}

const eliminaDuplicados = (arr) => {
  return arr.filter((valor, indice) => {
    return arr.indexOf(valor) === indice;
  });
}

fechas_no_duplicadas = eliminaDuplicados(fechas)              // Elimino valores duplicados --> van a ser mis labels

tipos_separados_agrup = {}

for (const [key, value] of Object.entries(tipos_seperados)) {
  tipos_separados_agrup[key] = _.groupBy(value, (b) => moment(b.fecha).startOf('month').format('YYYY/MM'))  // agrupo cada uno de ellos por fechas
}

datasets_final = {}

for (let f in fechas_no_duplicadas){
  if (tipos_separados_agrup["comision"][fechas_no_duplicadas[f]] !== undefined){
    console.log("SI")
    datasets_final["comision"][fec] = tipos_separados_agrup["comision"][fec].length
  }else{
    console.log("NO")
    datasets_final["comision"][fechas_no_duplicadas[fec]] = 0
  }
}



//https://bramantox.wordpress.com/2019/10/06/how-to-show-values-on-top-of-bars-in-chart-js/
var datasets = {
  labels: fechas_no_duplicadas,
  datasets: [{
      label: 'Users',
      backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
      borderColor: window.chartColors.red,
      borderWidth: 1,
      data: [53,117,79,56,45,89,61]
  }, {
      label: 'My Users',
      backgroundColor: color(window.chartColors.blue).alpha(0.5).rgbString(),
      borderColor: window.chartColors.blue,
      borderWidth: 1,
      data: [43,105,76,50,33,97,52]
  }]

};




let grouped_items = _.groupBy(data_informacion, (b) =>
  moment(b.fecha).startOf('month').format('YYYY/MM'));

let grouped_items = _.groupBy(data_informacion, (b) =>
  moment(b.fecha).startOf('month').format('YYYY/MM'));

_.values(grouped_items)
  .forEach(arr => arr.sort((a, b) => moment(a.fecha).day() - moment(b.fecha).day()));

console.log(grouped_items);

let data = []
for (const p in data_informacion){
    data.push(_.groupBy(data_informacion[p], (b) => moment(b.fecha).startOf('month').format('YYYY/MM')));
}


$(document).ready(function () {

    $("#item-grafico").on("click",function(){
      $(".secondary.menu a").attr("class","item");
      $(this).attr("class","active item");
      $("form").hide()
      $("#informacion").hide();
      $("#graficos").show();
      
      $("#row-graficos").empty();
  
      const labels = $.map(informacion, function(value, key) {
          return value.tipo;
      });
      const dias = $.map(informacion, function(value, key) {
          return value.cantidad;
        });

        console.log(labels)
        console.log(dias)
  
      const data = {
      labels: labels,
      datasets: [{
          axis: 'y',
          data: dias,
          backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(255, 159, 64, 0.2)',
          'rgba(255, 205, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(201, 203, 207, 0.2)'
          ],
          borderColor: [
          'rgb(255, 99, 132)',
          'rgb(255, 159, 64)',
          'rgb(255, 205, 86)',
          'rgb(75, 192, 192)',
          'rgb(54, 162, 235)',
          'rgb(153, 102, 255)',
          'rgb(201, 203, 207)'
          ],
          borderWidth: 1
      }]
      };
  
  
      $("#row-graficos").append('<canvas id="line-chart">');
      grafico = new Chart($("#line-chart"), {
          type: 'bar',
          data: data,
          options: {
              responsive: true,
              indexAxis: 'y',
              scales: {
                  yAxes: {
                    title: {
                      display: true,
                      text: 'Estados'
                    }
                  },
                  xAxes: {
                      title: {
                        display: true,
                        text: 'Cantidad de Dias en el Estado'
                      }
                  }
              },
        plugins: {
          legend: {
            display: false
          }
          }
            }
      });
    });

});