//var informacion = {'Industrial':{'Canon':{'Pago':255,'Cobro':320},'Infraccion':{'Pago':555,'Cobro':1233}},'Ganadero':{'Canon':{'Pago':432,'Cobro':676},'Infraccion':{'Pago':657,'Cobro':1234}}};
const motivo_dict = {"True":"Canon","False":"Infraccion"};

$(document).ready(function(){
            
    $("input[name='operaciones']").change(function() {
        dataset["operaciones"]=$("input[name=operaciones]").val();
        labels_filtros["operaciones"][1] = $("input[name=operaciones]").val();
    });

    $("input[name='motivos']").change(function() {
        dataset["motivos"]=$("input[name='motivos']").val();
        labels_filtros["motivos"][1]= $("input[name='motivos']").val().length>0 ? motivo_dict[$("input[name='motivos']").val()] : "";
    });

    $("[name='btn_tipo_reporte']").click(function(){
        var tipo_reporte = $(this).data('value');
        dataset['tipo_reporte']=tipo_reporte;
        console.log("apretaste boton: "+$(this).data('value'));
        $("#item-filtro").trigger("click"); 
    });
   
});