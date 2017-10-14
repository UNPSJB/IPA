$(document)
  .ready(function() {
    $('.ui.form')
      .form({
        fields: {
          username: {
            identifier  : 'username',
            rules: [
              {
                type   : 'empty',
                prompt : 'Por favor, ingrese el nombre de usuario'
              },
            ]
          },
          password: {
            identifier  : 'password',
            rules: [
              {
                type   : 'empty',
                prompt : 'Por favor, ingrese la contraseña'
              },
            ]
          }
        }
      })
    ;
    $( 'i.eye' ).hover( 
      function() {
        $(this).removeClass('disabled');
        $('.passwordInput').attr('type', 'text'); 
      }, 
      function() {
        $(this).addClass('disabled');
        $('.passwordInput').attr('type', 'password'); 
      }
    );
  });
