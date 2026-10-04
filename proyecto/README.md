# Clínica Peumina

Sistema web desarrollado como proyecto académico durante mi formación en Ingeniería en Informática.

El proyecto consiste en una aplicación para gestionar la información básica de una clínica médica ficticia, incluyendo pacientes, médicos, especialidades, citas e historial clínico.

La idea principal del proyecto fue poner en práctica el desarrollo de aplicaciones web utilizando Django, trabajando tanto en la lógica del backend como en la creación de las interfaces y la conexión con la base de datos.

Tecnologías utilizadas:

- Python 3
- Django 6
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Django Authentication

Funcionalidades:

Actualmente el sistema cuenta con las siguientes funcionalidades:

- Dashboard con información general y próximas citas.
- Registro y gestión de pacientes.
- Registro y gestión de médicos.
- Gestión de especialidades médicas.
- Creación y gestión de citas médicas.
- Cambio de estado de las citas:
  * Pendiente
  * Confirmada
  * Atendida
  * Cancelada
- Historial clínico asociado a los pacientes.
- Búsqueda y edición de información.
- Inicio de sesión y registro de usuarios.
- Panel de administración proporcionado por Django.
- Validaciones para evitar que un médico tenga dos citas en el mismo horario.
- Datos de prueba mediante un comando personalizado de Django.

Instalación y ejecución:

1.- Requisitos:

Para ejecutar el proyecto necesitas tener instalado:

* Python 3.10 o superior
* Git (opcional, pero recomendado)

2.- Clonar el repositorio:

git clone URL_DEL_REPOSITORIO
cd clinica-peumina

3.- Ejecutar las migraciones:

python manage.py migrate

4.- Cargar datos de prueba:

El proyecto incluye un comando para generar información de ejemplo, como especialidades, médicos, pacientes y citas.
python manage.py poblar_datos

Si el comando genera un usuario administrador, las credenciales de prueba son:

Usuario: admin
Contraseña: admin1234

También puedes crear tu propio usuario administrador utilizando:
python manage.py createsuperuser

5. Iniciar el servidor:
   
python manage.py runserver
Luego puedes acceder desde el navegador a:
http://127.0.0.1:8000/

6.- Accesos:

Sistema:
http://127.0.0.1:8000/login/

Panel de administración:
http://127.0.0.1:8000/admin/

7.-Base de datos:

Para este proyecto se utilizó SQLite, principalmente por su facilidad de configuración durante el desarrollo.
La base de datos se genera a partir de las migraciones de Django y se almacena localmente en:
db.sqlite3

8.- Consideraciones:

Este proyecto fue desarrollado con fines académicos y de aprendizaje, por lo que algunas configuraciones están pensadas para un entorno de desarrollo local.

9.- Mejoras futuras

Algunas funcionalidades que podrían incorporarse posteriormente son:

Generación de reportes en PDF o Excel.
Envío de correos para confirmar o cancelar citas.
Sistema de roles para médicos, recepcionistas y administradores.
Calendario para visualizar las horas médicas.
API REST utilizando Django REST Framework.
Mejoras en la interfaz y experiencia de usuario.
Despliegue de la aplicación en un servidor.

10.- Objetivo del proyecto:

Este proyecto me permitió poner en práctica conocimientos de desarrollo web, programación con Python y Django, manejo de bases de datos, creación de formularios, autenticación de usuarios y organización de un proyecto web.
También forma parte de mi proceso de aprendizaje y preparación profesional como estudiante de Ingeniería en Informática.

Desarrollado por Héctor Faraut López
Ingeniería en Informática

