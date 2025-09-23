Param(
    [string]$Port = "8000",
    [switch]$NoMigrate
)

Write-Host "=== Clinica Vet :: Modo SQLite ===" -ForegroundColor Cyan
if (Test-Path -Path .env) {
    Write-Host "Cargando variables desde .env" -ForegroundColor DarkCyan
    Get-Content .env | ForEach-Object {
        if ($_ -match '^[ \t]*#') { return }
        if ($_ -match '^[ \t]*$') { return }
        if ($_ -match '^(?<k>[^=#]+)=(?<v>.*)$') {
            $k = $Matches['k'].Trim()
            $v = $Matches['v'].Trim()
            [Environment]::SetEnvironmentVariable($k, $v)
        }
    }
}

# Forzamos SQLite ignorando lo que venga de .env
[Environment]::SetEnvironmentVariable('DB_ENGINE','django.db.backends.sqlite3')

if (-not $NoMigrate) {
    Write-Host "Aplicando migraciones (SQLite) ..." -ForegroundColor Yellow
    py -3 manage.py migrate
    if ($LASTEXITCODE -ne 0) { Write-Error "Error en migraciones"; exit 1 }
}

Write-Host "Iniciando servidor en http://127.0.0.1:$Port/ (SQLite)" -ForegroundColor Green
py -3 manage.py runserver 0.0.0.0:$Port