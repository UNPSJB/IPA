//var informacion = {'Industrial':{'Canon':{'Pago':255,'Cobro':320},'Infraccion':{'Pago':555,'Cobro':1233}},'Ganadero':{'Canon':{'Pago':432,'Cobro':676},'Infraccion':{'Pago':657,'Cobro':1234}}};
var informacion;
var canon_pago;
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

const motivo_dict = {"True":"Canon","False":"Infraccion"};

$(document).ready(function(){
    
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
            $("#informacion").show();
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



    
    $("#item-filtro").on("click",function(){
        $("#informacion").hide();
        $("#graficos").hide();
        $("form").show();

        $(".secondary.menu a").attr("class","item");
        $(this).attr("class","active item");
    });




   
});