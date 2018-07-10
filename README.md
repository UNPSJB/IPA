## Desarrollo de Software 2017 - ISFPP
### IPA - "Dirección General de Aguas - Permisos de Usos de Aguas"
### Organización: Instituto Provincial de Aguas
---

#### Cátedra
    * Lic. Diego van Haaster
    * Lic. Bruno Pazos

#### Alumnos
    * Alzugaray, Luciano
    * Bageler, Andrea
    * Castro, Federico 
    * Foletto, Lucas
    * Quinta, Carolina

----
## Como Instalarlo

Clona el repositorio en el directorio que desees
    
    git clone https://github.com/UNPSJB/IPA.git

Instala los requerimientos. Se recomienda utilizar un virtualenv para evitar conflictos de versiones con [virtualenv](https://virtualenv.pypa.io/).

    pip install -r requirements.txt

## Correr el servicio

Para correr el servidor, tan sólo utiliza las siguientes lineas: 

    cd IPA/
    python manage.py runserver 
    
El servicio debe estar corriendo en  http://localhost:8000/
