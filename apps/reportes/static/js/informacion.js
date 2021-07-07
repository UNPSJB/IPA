const tabla_head_rw1_th = {'':['Canon','Infraccion'],'True': ['Canon'],'False': ['Infraccion']}
const tabla_head_rw2_th = {'':['Pago','Cobro','Diferencia'],'Pago': ['Pago'],'Cobro': ['Cobro']}


$("#item-info").on("click",function(){
    $("form").hide();
    $("#graficos").hide();
    $(".secondary.menu a").attr("class","item");
    $(this).attr("class","active item");

    if (typeof informacion !== 'undefined'){
        $("#informacion").show();
        let tabla_head_rw1='<th class="descending" rowspan="2">Tipo Permiso</th>';
        let tabla_head_rw2='';
        let thrw1th = tabla_head_rw1_th[dataset["motivos"]];
        let thrw2th = tabla_head_rw2_th[dataset["operaciones"]];
        for (let rw1 of thrw1th){
            tabla_head_rw1 += '<th colspan='+tabla_head_rw2_th[dataset["operaciones"]].length+'>'+rw1+'</th>';
            for (let rw2 of thrw2th){
                tabla_head_rw2 += '<th>'+rw2+'</th>';
            }
            $("#tabla-head-rw2").empty().append(tabla_head_rw2);
        }
        $("#tabla-head-rw1").empty().append(tabla_head_rw1);
        
        $("#tabla-info").empty();
        $("tfoot").empty();
        for (let i in informacion){
            let str = '';
            for (let m of thrw1th){
                for (let o of thrw2th){
                    str += '<td>$'+informacion[i][m][o]+'</td>';
                }
            }
            $("#tabla-info").append('<tr><td>'+i+'</td>'+str+'</tr>');
        }
        $("#tabla-info tr:last-child").appendTo("tfoot");
        $("tfoot td").each(function() {
            $(this).replaceWith("<th>"+$(this).text()+"</th>");
        });
        $("tfoot tr").attr("class","active");
        $("#lista-filtros").empty();
        for(let lf in labels_filtros){
            if (labels_filtros[lf][1].length>0){
                $("#lista-filtros").append('<li>'+labels_filtros[lf][0]+': '+labels_filtros[lf][1]+'</li>')
            }
        }
    }

});