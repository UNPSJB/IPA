const eliminaDuplicados = (arr) => {
  return arr.filter((valor, indice) => {
    return arr.indexOf(valor) === indice;
  });
}

$(document).ready(function () {
    nombre_reporte = "Comisiones";
    tipo_reporte = "comisiones";
    $("#item-grafico").on("click",function(){
      $(".secondary.menu a").attr("class","item");
      $(this).attr("class","active item");
      $("form").hide()
      $("#informacion").hide();
      $("#graficos").show();
      
      $("#graficos").empty();
  

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
      
      fechas_no_duplicadas.sort(function(a, b){
        var aa = a.split('/').reverse().join(),
            bb = b.split('/').reverse().join();
        return aa < bb ? -1 : (aa > bb ? 1 : 0);
      });

      tipos_separados_agrup = {}
      
      for (const [key, value] of Object.entries(tipos_seperados)) {
        tipos_separados_agrup[key] = _.groupBy(value, (b) => moment(b.fecha).startOf('month').format('MM/YYYY'))  // agrupo cada uno de ellos por fechas
      }
      
      //var datasets_final = {"comision": {},'acta-de-inspeccion':{},'acta-de-infraccion':{}}
      var datasets_cantidades = {"comision": [],'acta-de-inspeccion':[],'acta-de-infraccion':[]}
      for(let ts in tipos_separados_agrup){
        for (let f in fechas_no_duplicadas){
          if (tipos_separados_agrup[ts][fechas_no_duplicadas[f]] !== undefined){
        //    datasets_final[ts][fechas_no_duplicadas[f]] = Object.keys(tipos_separados_agrup[ts][fechas_no_duplicadas[f]]).length
            datasets_cantidades[ts].push(Object.keys(tipos_separados_agrup[ts][fechas_no_duplicadas[f]]).length)
          }else{
          //  datasets_final[ts][fechas_no_duplicadas[f]] = 0
            datasets_cantidades[ts].push(0)
          }
        }
      }
      //console.log(datasets_final);
      console.log(datasets_cantidades);
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
    

      $("#graficos").append("<div class='chart-container' style='position: relative; height:30vh; width:60vw'><canvas id='line-chart'></div>");
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