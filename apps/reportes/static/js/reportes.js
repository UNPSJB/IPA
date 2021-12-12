var informacion;
var canon_pago;
var filtro_operaciones;
var filtro_motivos;
var dataset = { 'tipo_reporte': 'tipos_permisos',
'tipos_permisos': [],
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

function lista_filtros(){
    $("#lista-filtros").empty();
    for(let lf in labels_filtros){
        if (labels_filtros[lf][1].length>0){
            $("#lista-filtros").append('<li>'+labels_filtros[lf][0]+': '+labels_filtros[lf][1]+'</li>')
        }
    }
    if ($("#lista-filtros")[0].childElementCount==0){
        $("#lista-filtros").append('<li>No hay filtros seleccionados para este reporte</li>')
    }
}
/*
function printTablaTiposPermisos(){
    $('<iframe>', {
        name: 'f_tablas_permisos',
        class: 'printFrameTp'
    })
    .appendTo('body')
    .contents().find('body')
    .append("<h1>Reporte de "+ tipo_reporte +" - Tablas</h1>",$("#tabla-recaudacion"));

    window.frames['f_tablas_permisos'].focus();
    window.frames['f_tablas_permisos'].print();
    
    setTimeout(() => { $(".printFrameTp").remove(); }, 3);
}
*/

function printGrafico() {
    var grafico;

    if(["comisiones","gestion_de_permiso","tipos_permisos"].includes(tipo_reporte)){
        grafico = $("#line-chart");
        console.log("entre al grafico de"+tipo_reporte);
        if (tipo_reporte == "tipos_permisos"){
            grafico2 = $("#chart2");
        }else{
            grafico2 = "";
        }
    }else if (tipo_reporte == "series_temporales"){
        grafico = $("#chart3");
        grafico2 = "";
        console.log("entre al grafico de"+tipo_reporte);
    }else if (tipo_reporte == "proyeccion_valores_modulos"){
        grafico = $("#chart4");
        grafico2 = "";
        console.log("entre al grafico de"+tipo_reporte);
    }

    $('<iframe>', {
        name: 'myiframe',
        class: 'printFrame'
    })
    .appendTo('body')
    .contents().find('body')
    .append("<h1>Reporte de "+ nombre_reporte +" - Graficos</h1>",grafico,grafico2)
    .append("<h4>Este reporte se ha generado el "+moment().format("MM/DD/YYYY")+" a las "+moment().format("hh:mm:ss")+" por el usuario "+usuario_nombre+", "+usuario_apellido+"</h4>")
    
    if (tipo_reporte == "tipos_permisos"){
        $('<iframe>').append($("#chart2"));
    }
    
    window.frames['myiframe'].focus();
    window.frames['myiframe'].print();
    
    setTimeout(() => { $(".printFrame").remove(); }, 3);

}

$(document).ready(function(){
    filtro_operaciones = $("#filtro_operaciones");
    filtro_motivos = $("#filtro_motivos");

    $(".default.text").html("----------- Seleccionar opción -----------");
    $(".text").html("----------- Seleccionar opción -----------");

    $("select").change(function() {
        var str = "";
        $("select[name="+$(this).attr("name")+"] option:selected" ).each(function() {
            str += $(this).text() + " - ";
        });
        labels_filtros[$(this).attr("name")][1] = str.substring(0, str.length - 2);
        dataset[$(this).attr("name")] = $(this).val();
    });

    $("#item-filtro").on("click",function(){
        $("#informacion").hide();
        $("#graficos").hide();
        $("form").show();

        $(".secondary.menu a").attr("class","item");
        $(this).attr("class","active item");
    });

    $("#item-info-grafico").on("click",function(){
        $("#informacion").show();
        $("#graficos").show();
        $("form").hide();

        $(".secondary.menu a").attr("class","item");
        $(this).attr("class","active item");
    });

    $("#filtro-form").submit(function (e) {
        
        e.preventDefault();
        $.ajaxSettings.traditional = true;
        var url = $("form")[0].dataset["ajax_url"]
        if (url != '/reportes/gestion'){
            dataset["fecha_desde"]=$("input[name='daterange']").data('daterangepicker').startDate.format("YYYY-MM-DD");
            dataset["fecha_hasta"]=$("input[name='daterange']").data('daterangepicker').endDate.format("YYYY-MM-DD");
            labels_filtros["fechas"][1]=$("input[name='daterange']").data('daterangepicker').startDate.format("DD-MM-YYYY") 
                                        +" hasta "+ $("input[name='daterange']").data('daterangepicker').endDate.format("DD-MM-YYYY");        
        }

        $.get(url,dataset,function(data) {
            console.log(data)
            informacion = data;
            lista_filtros();
            $("#informacion").show();
            $("#item-info").trigger("click"); 
        });
    });

    $("#imprimir-tabla").bind("click", function(){
        if($("#item-info").attr("class")=='active item'){
            table.print(false, true);
        }else if ($("#item-grafico").attr("class")=='active item'){
            printGrafico();
        }else if ($("#item-info-grafico").attr("class")=='active item'){
            table.print(false, true);
            printGrafico();
        }
    });


    $("#descargar-tabla-json").bind("click", function(){
        table.download("json", "reporte.json");
    });
    $("#descargar-tabla-xlsx").bind("click", function(){
        table.download("xlsx", "reporte.xlsx", {title:"Reporte de "+ nombre_reporte, sheetName:"RepRecaudacionST"});
    });
    $("#descargar-tabla-pdf").bind("click", function(){
        table.download("pdf", "reporte.pdf", {title:"Reporte de "+ nombre_reporte, sheetName:"RepRecaudacionST"});
    });

});