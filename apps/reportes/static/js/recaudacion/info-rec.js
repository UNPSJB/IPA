var table;
const tabla_head_rw1_th = {'':['Canon','Infraccion'],'True': ['Canon'],'False': ['Infraccion']}
const tabla_head_rw2_th = {'':['Pago','Cobro','Diferencia'],'Pago': ['Pago'],'Cobro': ['Cobro']}
var informacion_tipos_permisos;


function info_tipos_permisos(){

    informacion_tipos_permisos = [];
    var data_informacion = $.extend(true,[], informacion);  //Hago copias de valores
    var indice=0;
    for (const [key, value] of Object.entries(data_informacion)) {
        
        if ((value["Canon"]["Cobro"]>0)||(value["Canon"]["Pago"]>0)||(value["Infraccion"]["Cobro"]>0)||(value["Infraccion"]["Pago"]>0)){
            informacion_tipos_permisos.push({
                'tipo':key,'motivo':'Canon','Cobro_Canon':value["Canon"]["Cobro"],'Diferencia_Canon':value["Canon"]["Diferencia"],'Pago_Canon':value["Canon"]["Pago"],
                'operacion':'Infraccion','Cobro_Infra':value["Infraccion"]["Cobro"],'Diferencia_Infra':value["Infraccion"]["Diferencia"],'Pago_Infra':value["Infraccion"]["Pago"]
            })
            indice += indice+1;
        }
    }
    

    table = new Tabulator("#tabla-temporal", {
        data: informacion_tipos_permisos,           //load row data from array
        //groupBy:"tipo",
        dataTree:true,
        layout:"fitColumns",      //fit columns to width of table
        responsiveLayout:"hide",  //hide columns that dont fit on the table
        tooltips:true,            //show tool tips on cells
        addRowPos:"top",          //when adding a new row, add it to the top of the table
        history:true,             //allow undo and redo actions on the table
        pagination:"local",       //paginate the data
        paginationSize:20,         //allow 7 rows per page of data
        movableColumns:true,      //allow column order to be changed
        resizableRows:true,       //allow row order to be changed

        columnHeaderVertAlign:"bottom", //align header contents to bottom of cell
        columns:[
        {title:"Tipo Permisos", field:"tipo",hozAlign:"center"},
        {//create column group
            title:"Canon",
            columns:[
                {title:"Pago", field:"Pago_Canon", hozAlign:"center",formatter:"money", formatterParams:{
                    precision:2,decimal:",",thousand:".",symbol:"$ ",
                }},
                {title:"Cobro", field:"Cobro_Canon", hozAlign:"center",formatter:"money", formatterParams:{
                    precision:2,decimal:",",thousand:".",symbol:"$ ",
                }},
                {title:"Diferencia", field:"Diferencia_Canon", hozAlign:"center",formatter:"money", formatterParams:{
                    precision:2,decimal:",",thousand:".",symbol:"$ ",
                }},
            ],
        },
        {//create column group
            title:"Infraccion",
            columns:[
                {title:"Pago", field:"Pago_Infra", hozAlign:"center",formatter:"money", formatterParams:{
                    precision:2,decimal:",",thousand:".",symbol:"$ ",
                }},
                {title:"Cobro", field:"Cobro_Infra", hozAlign:"center",formatter:"money", formatterParams:{
                    precision:2,decimal:",",thousand:".",symbol:"$ ",
                }},
                {title:"Diferencia", field:"Diferencia_Infra", hozAlign:"center",formatter:"money", formatterParams:{
                    precision:2,decimal:",",thousand:".",symbol:"$ ",
                }},
            ],
        },
        ],
        printAsHtml:true,
        printHeader:"<h1>Reportes de Recaudación - Tipos de Permisos - Tabla<h1>",
        printFooter:"<h4>Este reporte se ha generado el "+moment().format("MM/DD/YYYY")+" a las "+moment().format("hh:mm:ss")+" por el usuario "+usuario_nombre+", "+usuario_apellido+"</h4>",
        downloadConfig:{
            columnHeaders:true, //include column headers in downloaded table
            columnGroups:false, //do not include column groups in column headers for downloaded table
            rowGroups:false, //do not include row groups in downloaded table
            columnCalcs:true, //do not include column calcs in downloaded table
            dataTree:false, //do not include data tree in downloaded table
        },
    });

    $("#tabla-temporal").show();
    

}



function info_series_temporales(){
    console.log("Se ejecuta función de info_series");
    $("#tabla-recaudacion").hide();
    $("#tabla-temporal").show();
    var motivoCalc = function(values, data, calcParams){
        var canon = 0;
        var infra = 0;
    
        values.forEach(function(value){
            value == "Canon" ? canon++ : infra++;
        });
        return canon + " Canon | " + infra + " Infra";
    }

    var sumCalc = function(values, data, calcParams){
        var sum_total = 0;
        data.forEach(function(e){
            if(e.operacion == "Pago"){
                sum_total+=e.monto
            }else{
                sum_total-=e.monto
            }
        })
        return sum_total.toLocaleString('es-ar', {
            style: 'currency',
            currency: 'ARS',
            minimumFractionDigits: 2
        });
    }

    var data_informacion = $.extend(true,[], informacion);

    table = new Tabulator("#tabla-temporal", {
        data:data_informacion,           //load row data from array
        groupBy:"tipo",
        dataTree:true,
        layout:"fitColumns",      //fit columns to width of table
        responsiveLayout:"hide",  //hide columns that dont fit on the table
        tooltips:true,            //show tool tips on cells
        addRowPos:"top",          //when adding a new row, add it to the top of the table
        history:true,             //allow undo and redo actions on the table
        pagination:"local",       //paginate the data
        paginationSize:20,         //allow 7 rows per page of data
        movableColumns:true,      //allow column order to be changed
        resizableRows:true,       //allow row order to be changed

        columns:[                 //define the table columns
            {title:"Fecha", field:"fecha", mutator:function(value, data, type, mutatorParams, cell){
                return moment(value , "YYYY/MM/DD").format("DD/MM/YYYY");
            },hozAlign:"center",headerHozAlign:"center"},
            {title:"Tipo Permiso", field:"tipo",visible:true,hozAlign:"center",headerHozAlign:"center"},
            {title:"Motivo", field:"motivo", mutator:function(value, data, type, mutatorParams, cell){
                return value ? "Canon" : "Infracción"
            },bottomCalc:motivoCalc,hozAlign:"center",headerHozAlign:"center"},
            {title:"Monto", field:"monto",formatter:"money", bottomCalc:sumCalc, formatterParams:{
                precision:2,decimal:",",thousand:".",symbol:"$ ",
            },hozAlign:"right",headerHozAlign:"center"},
            {title:"Operación", field:"operacion",hozAlign:"center",headerHozAlign:"center"},
        ],
        printAsHtml:true,
        printHeader:"<h1>Reportes de Recaudación - Serie Temporal - Tabla<h1>",
        printFooter:"<h4>Este reporte se ha generado el "+moment().format("MM/DD/YYYY")+" a las "+moment().format("hh:mm:ss")+" por el usuario "+usuario_nombre+", "+usuario_apellido+"</h4>",
        downloadConfig:{
            columnHeaders:true, //include column headers in downloaded table
            columnGroups:false, //do not include column groups in column headers for downloaded table
            rowGroups:false, //do not include row groups in downloaded table
            columnCalcs:true, //do not include column calcs in downloaded table
            dataTree:false, //do not include data tree in downloaded table
        },
    });

    
}

function info_proyeccion_vm(){
    console.log("Se ejecuta función de info proyeccion valores");
    console.log(informacion);
    $("#tabla-recaudacion").hide();
    $("#tabla-temporal").show();
    var data_informacion = $.extend(true,[], informacion);

    table = new Tabulator("#tabla-temporal", {
        data:data_informacion,           //load row data from array
        groupBy:"tipo",
        dataTree:true,
        layout:"fitColumns",      //fit columns to width of table
        responsiveLayout:"hide",  //hide columns that dont fit on the table
        tooltips:true,            //show tool tips on cells
        addRowPos:"top",          //when adding a new row, add it to the top of the table
        history:true,             //allow undo and redo actions on the table
        pagination:"local",       //paginate the data
        paginationSize:20,         //allow 7 rows per page of data
        movableColumns:true,      //allow column order to be changed
        resizableRows:true,       //allow row order to be changed

        columns:[                 //define the table columns
            {title:"Fecha de Módulo", field:"fecha", mutator:function(value, data, type, mutatorParams, cell){
                return moment(value , "YYYY/MM/DD").format("DD/MM/YYYY");
            },hozAlign:"center",headerHozAlign:"center"},
            {title:"Valor de Módulo", field:"v_modulo",formatter:"money", formatterParams:{
                precision:2,decimal:",",thousand:".",symbol:"$ ",
            },hozAlign:"right",headerHozAlign:"center"},
            {title:"Fecha de Calculo", field:"fdesde", mutator:function(value, data, type, mutatorParams, cell){
                return moment(value , "YYYY/MM/DD").format("DD/MM/YYYY");
            },hozAlign:"center",headerHozAlign:"center"},
            {title:"Vencimiento del Permiso", field:"fvenc", mutator:function(value, data, type, mutatorParams, cell){
                return moment(value , "YYYY/MM/DD").format("DD/MM/YYYY");
            },hozAlign:"center",headerHozAlign:"center"},
            {title:"Monto", field:"monto",formatter:"money", formatterParams:{precision:2,decimal:",",thousand:".",symbol:"$ "},
            bottomCalc:"sum", bottomCalcFormatter: "money",
            bottomCalcFormatterParams:{precision:2,decimal:",",thousand:".",symbol:"$ "},
            hozAlign:"right",headerHozAlign:"center"},
            {title:"Estado", field:"estado",hozAlign:"center",headerHozAlign:"center"},
            //{title:"Tipo Permiso", field:"tipo",visible:true,hozAlign:"center",headerHozAlign:"center"},
        ],
        printAsHtml:true,
        printHeader:"<h1>Reportes de Recaudación - Proyección por Valor de Módulo - Tabla<h1>",
        printFooter:"<h4>Este reporte se ha generado el "+moment().format("MM/DD/YYYY")+" a las "+moment().format("hh:mm:ss")+" por el usuario "+usuario_nombre+", "+usuario_apellido+"</h4>",
        downloadConfig:{
            columnHeaders:true, //include column headers in downloaded table
            columnGroups:false, //do not include column groups in column headers for downloaded table
            rowGroups:false, //do not include row groups in downloaded table
            columnCalcs:true, //do not include column calcs in downloaded table
            dataTree:false, //do not include data tree in downloaded table
        },
    });
}

$("#item-info").on("click",function(){
    $("form").hide();
    $("#graficos").hide();
    $(".secondary.menu a").attr("class","item");
    $(this).attr("class","active item");

    if (typeof informacion !== 'undefined'){
        $("#informacion").show();

        switch (dataset['tipo_reporte']) {
            case "tipos_permisos": info_tipos_permisos(); break;
            case "series_temporales": info_series_temporales(); break;
            case "proyeccion_valores_modulos": info_proyeccion_vm(); break;
        }



    }

});