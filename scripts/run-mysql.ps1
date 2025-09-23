Param(
    [string]$Port = "8000",
    [switch]$NoMigrate,
    [switch]$ForceMariaCompatibility
)

Write-Host "=== Clinica Vet :: Modo MySQL/MariaDB ===" -ForegroundColor Cyan
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

# Forzar engine MySQL si no está definido
if (-not [Environment]::GetEnvironmentVariable('DB_ENGINE')) {
    [Environment]::SetEnvironmentVariable('DB_ENGINE','django.db.backends.mysql')
}

if ($ForceMariaCompatibility) {
    Write-Host "(Compat) Usando Django 4.2.x para MariaDB <10.5" -ForegroundColor DarkYellow
}

$dbHost = [Environment]::GetEnvironmentVariable('DB_HOST')
$dbName = [Environment]::GetEnvironmentVariable('DB_NAME')
Write-Host "DB_HOST=$dbHost DB_NAME=$dbName" -ForegroundColor DarkGray

if (-not $NoMigrate) {
    Write-Host "Aplicando migraciones (MySQL/MariaDB)..." -ForegroundColor Yellow
    py -3 manage.py migrate
    if ($LASTEXITCODE -ne 0) { Write-Error "Error en migraciones"; exit 1 }
}

Write-Host "Iniciando servidor en http://127.0.0.1:$Port/ (MySQL/MariaDB)" -ForegroundColor Green
py -3 manage.py runserver 0.0.0.0:$Port