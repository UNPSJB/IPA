$(document).ready(function() {
    $('.ui.form').form({
        on: 'blur',
        fields: {
          empleados: {
        identifier  : 'empleados',
        rules: [
          {
            type   : 'minCount[1]',
            prompt : 'Ingrese al menos 1 empleados'
          },
          {
            type   : 'empty',
             prompt : 'Por favor, ingrese el nombre de usuario'
          }
        ]
      }}
         
      });//end form
  }); //End ready
