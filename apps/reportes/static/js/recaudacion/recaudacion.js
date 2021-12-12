//var informacion = {'Industrial':{'Canon':{'Pago':255,'Cobro':320},'Infraccion':{'Pago':555,'Cobro':1233}},'Ganadero':{'Canon':{'Pago':432,'Cobro':676},'Infraccion':{'Pago':657,'Cobro':1234}}};
const motivo_dict = {"True":"Canon","False":"Infraccion"};
var filtro_operaciones;
var filtro_motivos;

const dict_nombre_reporte = {
    'tipos_permisos': 'Tipos de Permisos',
    'series_temporales': 'Series Temporales',
    'proyeccion_valores_modulos': 'Proyeccion Valores de Modulos'
}

$(document).ready(function(){
    tipo_reporte = "tipos_permisos";
    nombre_reporte= dict_nombre_reporte[tipo_reporte];
    
    $('#filtro_operaciones').parent().parent().prop('hidden', true);
    $('#filtro_motivos').parent().parent().prop('hidden', true);

    $("input[name='operaciones']").change(function() {
        dataset["operaciones"]=$("input[name=operaciones]").val();
        labels_filtros["operaciones"][1] = $("input[name=operaciones]").val();
    });

    $("input[name='motivos']").change(function() {
        dataset["motivos"]=$("input[name='motivos']").val();
        labels_filtros["motivos"][1]= $("input[name='motivos']").val().length>0 ? motivo_dict[$("input[name='motivos']").val()] : "";
    });

    $("[name='btn_tipo_reporte']").click(function(){
        tipo_reporte = $(this).data('value');
        nombre_reporte= dict_nombre_reporte[tipo_reporte];
        
        dataset['tipo_reporte']=tipo_reporte;
        console.log("apretaste boton: "+$(this).data('value'));
        $('#filtro_operaciones').parent().parent().prop('hidden', false);
        $('#filtro_motivos').parent().parent().prop('hidden', false);

        if($(this).data('value')!='series_temporales'){
            $('#filtro-form > div:nth-child(2) > div > div.text')[0].innerHTML = '----------- Seleccionar opción -----------';
            $('#filtro_operaciones')[0].value = '';
            $('#filtro_operaciones').parent().parent().prop('hidden', true);
            $('#filtro-form > div:nth-child(3) > div > div.text')[0].innerHTML = '----------- Seleccionar opción -----------';
            $('#filtro_motivos')[0].value = '';
            $('#filtro_motivos').parent().parent().prop('hidden', true);
        }

        $("#item-filtro").trigger("click"); 
    });
   
});