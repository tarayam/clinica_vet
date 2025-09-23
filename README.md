Clinica Vet
=============

Proyecto Django de ejemplo para la clínica veterinaria.

Requisitos
---------
- Python 3.11+ (probado con 3.13)
- virtualenv (recomendado)
- MySQL/MariaDB (opcional) o SQLite (por defecto fácil)

Instalación rápida (Windows / PowerShell)
---------------------------------------
1. Crear y activar entorno virtual:

```powershell
python -m venv .venV
.\.venV\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Configurar variables de entorno (no almacenar secretos en el repo):
- `SECRET_KEY`
- Credenciales de la base de datos (si usas MySQL)

4. Ejecutar migraciones y crear superusuario:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. Ejecutar servidor:

```powershell
python manage.py runserver
```

Notas
-----
- No subas archivos con credenciales ni el `SECRET_KEY`.
- Se recomienda usar un archivo `.env` excluido por `.gitignore` para variables sensibles.

Uso con Docker (desarrollo)
--------------------------
Este proyecto incluye un `Dockerfile` y `docker-compose.yml` para levantar un servicio web y una base MySQL para desarrollo.

1. Copia el archivo de ejemplo y ajusta valores:

```powershell
copy .env.example .env
```

2. Levantar los servicios:

```powershell
docker compose up --build
```

3. Ejecutar migraciones dentro del contenedor web (opcional si no están aplicadas):

```powershell
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Notas Docker
------------
- La base MySQL queda accesible en el servicio `db` dentro de la red de Docker. Las variables en `.env` se usan en `docker-compose.yml`.
- No uses este `docker-compose` en producción sin asegurar contraseñas y ajustes de persistencia/backups.

Uso con XAMPP (MySQL/MariaDB local)
-----------------------------------
Si usas XAMPP, el servicio MySQL suele correr como MariaDB y escucha en `127.0.0.1:3306`.

1. Inicia el módulo MySQL desde el panel de XAMPP.
2. (Opcional) Crea base y usuario dedicados (o usa `root` sin password si es sólo local):
```sql
CREATE DATABASE clinica_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'clinica_user'@'localhost' IDENTIFIED BY 'ClinicaPass123';
GRANT ALL PRIVILEGES ON clinica_db.* TO 'clinica_user'@'localhost';
FLUSH PRIVILEGES;
```
3. Crea un archivo `.env` (NO lo subas) basado en `.env.example` y ajusta:
```
DB_ENGINE=django.db.backends.mysql
DB_HOST=127.0.0.1
DB_PORT=3306
# Si usas root sin password:
DB_USER=root
DB_PASSWORD=
```
4. Instala dependencias (ya hecho si seguiste pasos previos) y aplica migraciones:
```powershell
py -3 manage.py migrate
```
5. Inicia el servidor:
```powershell
py -3 manage.py runserver
```

Notas XAMPP
-----------
- Si obtienes error de versión (MariaDB 10.4.x) con Django 5+, mantén Django 4.2 LTS (ya fijado en `requirements.txt`).
- Asegúrate de que no haya otro servicio ocupando el puerto 3306.
- Si cambias a MySQL 8 / MariaDB 10.5+, podrás subir de versión Django más adelante.

Forzar uso de SQLite temporalmente
---------------------------------
Si la base MySQL no está lista o da errores, puedes usar SQLite rápido:
```powershell
$env:DB_ENGINE='django.db.backends.sqlite3'; py -3 manage.py migrate; py -3 manage.py runserver
```
O fija `DB_ENGINE=django.db.backends.sqlite3` en tu `.env`.

Scripts de ayuda (PowerShell)
-----------------------------
Se añadieron scripts en `scripts/` para facilitar el arranque:

1. Modo SQLite rápido:
```powershell
pwsh ./scripts/run-sqlite.ps1
```
	Parámetros opcionales:
	- `-Port 9000` cambia el puerto.
	- `-NoMigrate` salta migraciones.

2. Modo MySQL/MariaDB (XAMPP o Docker):
```powershell
pwsh ./scripts/run-mysql.ps1
```
	Parámetros opcionales:
	- `-Port 9000`
	- `-NoMigrate`
	- `-ForceMariaCompatibility` (solo mensaje recordatorio si usas MariaDB <10.5)

Ambos scripts:
- Cargan variables desde `.env` si existe (ignorando líneas comentadas).
- Muestran información básica antes de levantar el servidor.

Si tu política de ejecución bloquea los scripts:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
