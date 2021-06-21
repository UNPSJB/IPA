$(document).ready(function(){
    $(".default.text").html("----------- Seleccionar opción -----------");
    $("#ingresos-form").submit(function (e) {
        e.preventDefault();
        var tipos = $("select[name='tipos_permisos']").val()
        var operaciones = $("input[name='operaciones']").val()
        var motivos = $("input[name='motivos']").val()
        var fecha_desde = $("input[name='daterange']").data('daterangepicker').startDate.format("YYYY-MM-DD")
        var fecha_hasta = $("input[name='daterange']").data('daterangepicker').endDate.format("YYYY-MM-DD")
        
        var afluentes = $("select[name='afluentes']").val()
        var localidades = $("select[name='localidades']").val()
        var departamentos = $("select[name='departamentos']").val()

        
        var url = $("form")[0].dataset["ajax_url"]

        $.ajaxSettings.traditional = true;
        var dataset = { 'tipo_permiso': tipos,
                        'operaciones': operaciones,
                        'motivos': motivos,
                        'fecha_desde': fecha_desde,
                        'fecha_hasta':fecha_hasta,
                        'afluentes':afluentes,
                        'localidades':localidades,
                        'departamentos':departamentos} 


        console.log(dataset)
        $.get(url,dataset,function( data ) {
            console.log(data)

          }); 
    });
    
   
});