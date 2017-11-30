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
      });//end form