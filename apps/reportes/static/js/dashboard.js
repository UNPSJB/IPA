$(document).ready(function(){

    var myChart5 = new Chart($("#real-line-chart"), {
        type:'line',
        data:{
            labels: ['Enero-21','Febrero-21','Marzo-21','Abril-21','Mayo-21','Junio-21','Julio-21'],
            datasets: [{
                label: 'Pagos realizados de Canon',
                data: [300, 100, 1500, 2300, 3500, 6000, 8000],
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },{
                label: 'Cobros realizados de Canon',
                data: [300, 500, 3500, 4300, 5500, 7000, 9500],
                fill: false,
                borderColor: 'rgb(75, 255, 192)',
                tension: 0.1
            }]
        }
    });

    var myChart6 = new Chart($("#proyec-line-chart"), {
        type:'line',
        data:{
            labels: ['Agosto-21','Septiembre-21','Octubre-21','Noviembre-21','Diciembre-21','Enero-22'],
            datasets: [{
                label: 'Pagos proyectados de Canon',
                data: [10000, 11500, 12300, 13500, 16000, 18000],
                fill: false,
                borderColor: 'rgb(255, 185, 192)',
                tension: 0.1
            },{
                label: 'Cobros proyectados de Canon',
                data: [11000, 12500, 15300, 18500, 20000, 28000],
                fill: false,
                borderColor: 'rgb(255, 50, 50)',
                tension: 0.1
            }]
        }
    });
   
});