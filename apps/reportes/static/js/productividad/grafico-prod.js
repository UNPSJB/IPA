
$(document).ready(function () {
    console.log(informacion);
    console.log(typeof(informacion));

    $("#item-grafico").on("click",function(){
      $(".secondary.menu a").attr("class","item");
      $(this).attr("class","active item");
      $("form").hide()
      $("#informacion").hide();
      $("#graficos").show();
      
      $("#row-graficos").empty();
  
      const labels = $.map(informacion, function(value, key) {
          return value.estado;
      });
      const dias = $.map(informacion, function(value, key) {
          return value.dias;
        });
  
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