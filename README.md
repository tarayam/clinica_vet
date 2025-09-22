Clinica Vet
=============

Proyecto Django de ejemplo para la clínica veterinaria.

Requisitos
---------
- Python 3.11+
- virtualenv (recomendado)
- MySQL (opcional) o SQLite

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
