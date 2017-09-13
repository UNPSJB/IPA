$(document)
  .ready(function() {
    $('.ui.form')
      .form({
        fields: {
          email: {
            identifier  : 'email',
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
  })
;
