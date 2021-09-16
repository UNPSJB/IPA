

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
            //$("#informacion").show();
            //$("#item-info").trigger("click"); 
        });
    });
});