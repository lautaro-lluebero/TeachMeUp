# TeachMeUp

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
