# TeachMeUp
TeachMeUp es una página web pensada para facilitar el encuentro entre alumnos y profesores particulares.
Desde el menú podes navegar entre el inicio y el listado de profesores, filtrar por materia, zona y modalidad (virtual, presencial o mixta) y ver en cada tarjeta el nombre del docente, la asignatura, el nivel y el precio por hora.
El objetivo de la plataforma es que cualquier estudiante pueda encontrar rápidamente un profesor adecuado y empezar a tomar clases de manera simple y segura. Y por el lado de profesores poder brindar un espacio compartido donde puedan compartir materiales, experiencias e inquietudes con seguridad.
Tecnologías utilizadas: Python, MySQL, Flask, HTML, CSS, JavaScript.

Integrantes del proyecto: Francisco Iglesias, Jazmin Benitez, Lautaro Lluebero, Máximo Mercau y Santino Barrionuevo.

## Requisitos

- Python 3
- MySQL

## Configuración del entorno

### 1. Crear un entorno virtual

#### En Linux / macOS:

```sh
python3 -m venv <nombre_del_entorno>
```

#### En Windows:

```sh
python -m venv <nombre_del_entorno>
```

### 2. Activar el entorno virtual

#### En Linux / macOS:

```sh
source <nombre_del_entorno>/bin/activate
```

#### En Windows:

```sh
<nombre_del_entorno>\Scripts\activate
```

### 3. Instalar dependencias

```sh
pip install Flask Flask-SQLAlchemy PyMySQL python-dotenv
```

```sh
pip install cryptography
```

```sh
pip install requests
```

## Configuración de la base de datos

Antes de ejecutar la aplicación, debes configurar las siguientes variables de entorno:

```sh
MYSQL_USER=<tu_usuario>
MYSQL_PASSWORD=<tu_contraseña>
MYSQL_HOST=<host_de_mysql>
MYSQL_PORT=<puerto_de_mysql>
MYSQL_DB=<nombre_de_la_base_de_datos>
```

## Instalación y ejecución

1. Clona el repositorio:

```sh
git clone <url_del_repositorio>
```

2. Accede al directorio del proyecto:

```sh
cd <nombre_del_proyecto>
```

3. Instala las dependencias desde el archivo `requirements.txt`:

```sh
pip install -r requirements.txt
```

4. Ejecuta la aplicación:

```sh
python app.py
```
