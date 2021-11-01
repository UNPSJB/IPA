

$(document).ready(function(){
    $(".default.text").html("----------- Seleccionar opción -----------");
    $(".text").html("----------- Seleccionar opción -----------");

    $("#filtro-recaudacion-form").submit(function (e) {
        e.preventDefault();
        $.ajaxSettings.traditional = true;
        console.log("apretaste boton");

        var url = $("form")[0].dataset["ajax_url"]

        $.get(url,function( data ) {
            //informacion = data;
            console.log(data);
            _.groupBy(data, (dt) => moment(dt).month());
            //$("#informacion").show();
            //$("#item-info").trigger("click"); 
        });
    });


    const data = [
        "2021-10-11 09:07:21",
        "2021-10-10 10:03:51",
        "2021-10-07 02:07:02",
        "2021-11-27 08:02:45",
        "2021-11-19 01:02:32",
        "2021-12-01 22:13:21",
        "2021-02-12 09:07:21",
        "2021-05-18 04:02:29",
        "2021-05-21 14:01:42",
        "2021-07-11 01:16:29","2021-09-30 01:16:29","2021-09-29 01:16:29","2021-09-27 01:16:29"
     ];
     
     _.groupBy(data, (dt) => moment(dt).month());

});