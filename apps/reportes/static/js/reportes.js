var informacion;
var canon_pago;

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

$(document).ready(function(){

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
        dataset["fecha_desde"]=$("input[name='daterange']").data('daterangepicker').startDate.format("YYYY-MM-DD");
        dataset["fecha_hasta"]=$("input[name='daterange']").data('daterangepicker').endDate.format("YYYY-MM-DD");
        labels_filtros["fechas"][1]=$("input[name='daterange']").data('daterangepicker').startDate.format("DD-MM-YYYY") 
                                    +" hasta "+ $("input[name='daterange']").data('daterangepicker').endDate.format("DD-MM-YYYY");        

        var url = $("form")[0].dataset["ajax_url"]
        console.log(url+"sasd");
        $.get(url,dataset,function(data) {
            console.log(data)
            informacion = data;
            $("#informacion").show();
            $("#item-info").trigger("click"); 
        });
    });

    $("#imprimir-tabla").bind("click", function(){
        table.print(false, true);
    });

    $("#descargar-tabla-json").bind("click", function(){
        table.download("json", "reprecaudacionst.json");
    });
    $("#descargar-tabla-xlsx").bind("click", function(){
        table.download("xlsx", "reprecaudacionst.xlsx", {sheetName:"RepRecaudacionST"});
    });
    $("#descargar-tabla-pdf").bind("click", function(){
        table.download("pdf", "reprecaudacionst.pdf", {sheetName:"RepRecaudacionST"});
    });
});