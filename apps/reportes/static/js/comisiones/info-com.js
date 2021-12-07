var table;

$("#item-info").on("click",function(){
    $("form").hide();
    $("#graficos").hide();
    $(".secondary.menu a").attr("class","item");
    $(this).attr("class","active item");

    if (typeof informacion !== 'undefined'){
        $("#informacion").show();
        var data_informacion = $.extend(true,[], informacion);
        console.log(data_informacion)
        console.log(data_informacion)
        console.log(data_informacion)

        table = new Tabulator("#tabla", {
            data:data_informacion,           //load row data from array
            layout:"fitColumns",      //fit columns to width of table
            responsiveLayout:"hide",  //hide columns that dont fit on the table
            tooltips:true,            //show tool tips on cells
            addRowPos:"top",          //when adding a new row, add it to the top of the table
            history:true,             //allow undo and redo actions on the table
            movableColumns:true,      //allow column order to be changed
            resizableRows:true,       //allow row order to be changed
    
            columns:[                 //define the table columns
                {title:"Comisiones", field:"comisiones", hozAlign:"center",headerHozAlign:"center"},
                {title:"Actas de Infracción", field:"actas_de_infraccion",hozAlign:"right",headerHozAlign:"center"},
                {title:"Actas de Inspeccion", field:"actas_de_inspeccion",hozAlign:"right",headerHozAlign:"center"},
            ],
            printAsHtml:true,
            printHeader:"<h1>Reporte de Comisiones vs Actas <h1>",
            printFooter:"<h4>"+"Este reporte se ha impreso el "+moment().format("MM/DD/YYYY")+" a las "+moment().format("hh:mm:ss")+".<h2>",
            downloadConfig:{
                columnHeaders:true, //include column headers in downloaded table
                columnGroups:false, //do not include column groups in column headers for downloaded table
                rowGroups:false, //do not include row groups in downloaded table
                columnCalcs:true, //do not include column calcs in downloaded table
                dataTree:false, //do not include data tree in downloaded table
            },
        });
    }

});