$(document).ready(function(){
    const motivo_dict = {"True":"Canon","False":"Infraccion"};
    var informacion;
    var dataset = { 'tipos_permisos': [],
    'operaciones': '',
    'motivos': '',
    'fecha_desde': '',
    'fecha_hasta': '',
    'afluentes': [],
    'localidades': [],
    'departamentos': []} 

    var labels_filtros = {'tipos_permisos':['TIPO DE PERMISOS',''], 'operaciones':['OPERACIONES',''], 
                            'motivos':['MOTIVOS DE OPERACION',''], 'afluentes':['AFLUENTES',''],'localidades':['LOCALIDADES',''],  
                            'departamentos':['DEPARTAMENTOS',''],'fechas':['FECHAS', ''],};

    $(".default.text").html("----------- Seleccionar opción -----------");
    $(".text").html("----------- Seleccionar opción -----------");

    $("#filtro-recaudacion-form").submit(function (e) {
        e.preventDefault();
        $.ajaxSettings.traditional = true;
        dataset["fecha_desde"]=$("input[name='daterange']").data('daterangepicker').startDate.format("YYYY-MM-DD");
        dataset["fecha_hasta"]=$("input[name='daterange']").data('daterangepicker').endDate.format("YYYY-MM-DD");
        dataset["motivos"]=$("input[name='motivos']").val();
        labels_filtros["motivos"][1]= $("input[name='motivos']").val().length>0 ? motivo_dict[$("input[name='motivos']").val()] : "";
        labels_filtros["fechas"][1]=$("input[name='daterange']").data('daterangepicker').startDate.format("DD-MM-YYYY") 
                                    +" hasta "+ $("input[name='daterange']").data('daterangepicker').endDate.format("DD-MM-YYYY");        
        var url = $("form")[0].dataset["ajax_url"]

        $.get(url,dataset,function( data ) {
            informacion = data;
            $("#item-info").trigger("click"); 
        });
    });
    
    $("select").change(function() {
        var str = "";
        $("select[name="+$(this).attr("name")+"] option:selected" ).each(function() {
            str += $(this).text() + " - ";
        });
        labels_filtros[$(this).attr("name")][1] = str.substring(0, str.length - 2);
        dataset[$(this).attr("name")] = $(this).val()
    });
    
    $("input[name='operaciones']").change(function() {
        dataset["operaciones"]=$("input[name=operaciones]").val();
        labels_filtros["operaciones"][1] = $("input[name=operaciones]").val();
    });


    $("#item-info").on("click",function(){
        $("form").hide();
        $("#informacion").show();
        $("#tabla-head-rw1").empty().append('<th class="descending" rowspan="2">Tipo Permiso</th><th colspan="3">Canon</th><th colspan="3">Infracción</th>');
        $("#tabla-head-rw2").empty().append('<th >Pagado</th> <th>Cobrado</th> <th>Diferencia</th><th>Pagado</th><th>Cobrado</th><th>Diferencia</th>');
        $("#tabla-info").empty();
        $("tfoot").empty();
        for (let p in informacion){
            $("#tabla-info").append('<tr><td>'+p+'</td><td>$'+informacion[p]['Canon']['Pago']+'</td><td>$'+informacion[p]['Canon']['Cobro']+'</td> \
                            <td>$'+informacion[p]['Canon']['Diferencia']+'</td><td>$'+informacion[p]['Infraccion']['Pago']+'</td> \
                            <td>$'+informacion[p]['Infraccion']['Cobro']+'</td><td>$'+informacion[p]['Infraccion']['Diferencia']+'</td></tr>');
        }
        $("#tabla-info tr:last-child").appendTo("tfoot");
        $("tfoot td").each(function() {
            $(this).replaceWith("<th>"+$(this).text()+"</th>");
        });
        $("tfoot tr").attr("class","active");
        $(".secondary.menu a").attr("class","item");
        $(this).attr("class","active item");
        $("#lista-filtros").empty();
        for(let lf in labels_filtros){
            if (labels_filtros[lf][1].length>0){
                $("#lista-filtros").append('<li>'+labels_filtros[lf][0]+': '+labels_filtros[lf][1]+'</li>')
            }
        }
    });
    
    $("#item-filtro").on("click",function(){
        $("#informacion").hide();
        $("form").show();

        $(".secondary.menu a").attr("class","item");
        $(this).attr("class","active item");
        console.log("boton de filtro apretado");
    });

    $("#item-info-grafico").on("click",function(){
        $("form").hide()
        $(".secondary.menu a").attr("class","item");
        $(this).attr("class","active item");
        console.log("boton de informacion apretado");
    });

    $("#item-grafico").on("click",function(){
        $("form").hide()
        $(".secondary.menu a").attr("class","item");
        $(this).attr("class","active item");
        console.log("boton de informacion apretado");
    });
   
});