<#
    Arranque diario del asistente documental de INTEREMPREX.

    Un solo comando: comprueba el entorno, se asegura de que Ollama responde y
    abre el asistente. Pensado para la terminal PowerShell de F, incluida la
    terminal remota de VS Code conectada a ordenador-f.

    No instala nada, no cambia la politica de PowerShell y no crea servicios ni
    tareas de inicio de Windows. Al terminar el asistente deja Ollama en marcha
    para que la siguiente consulta no tenga que esperar la carga del modelo.
#>

$ErrorActionPreference = "Stop"

# --- 1. Localizar el proyecto desde la posicion de este mismo archivo --------
# Asi funciona aunque se ejecute desde otra carpeta o por ruta completa.
$Proyecto = $PSScriptRoot
$Python = Join-Path $Proyecto ".venv\Scripts\python.exe"
$Asistente = Join-Path $Proyecto "asistente_documental.py"
$CarpetaLogs = Join-Path $Proyecto "logs"

$ApiVersion = "http://127.0.0.1:11434/api/version"
$SegundosEspera = 30

Write-Host ""
Write-Host "Asistente documental de INTEREMPREX" -ForegroundColor Cyan
Write-Host "Equipo: $env:COMPUTERNAME   Proyecto: $Proyecto"
Write-Host ""

# --- 2. Comprobar que el entorno del proyecto esta donde se espera -----------
if (-not (Test-Path $Python)) {
    Write-Host "ERROR: no encuentro el Python del proyecto." -ForegroundColor Red
    Write-Host "  Esperaba: $Python"
    Write-Host "  El entorno virtual .venv no esta creado o la carpeta no es la correcta."
    Write-Host "  Comprueba que estas en la carpeta original del proyecto en F."
    exit 1
}
if (-not (Test-Path $Asistente)) {
    Write-Host "ERROR: no encuentro asistente_documental.py." -ForegroundColor Red
    Write-Host "  Esperaba: $Asistente"
    exit 1
}
Write-Host "[1/3] Entorno del proyecto correcto." -ForegroundColor Green

# --- 3. Ollama: reutilizar si ya responde, arrancarlo si no ------------------
function Test-Ollama {
    try {
        $r = Invoke-RestMethod -Uri $ApiVersion -TimeoutSec 3
        return $r.version
    } catch {
        return $null
    }
}

$version = Test-Ollama
if ($version) {
    Write-Host "[2/3] Ollama ya estaba activo (version $version). Se reutiliza." -ForegroundColor Green
} else {
    Write-Host "[2/3] Ollama no responde. Buscando la instalacion existente..."

    $candidatos = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"),
        (Join-Path $env:ProgramFiles "Ollama\ollama.exe")
    )
    $exe = $null
    foreach ($c in $candidatos) {
        if (Test-Path $c) { $exe = $c; break }
    }
    if (-not $exe) {
        $enPath = Get-Command ollama -ErrorAction SilentlyContinue
        if ($enPath) { $exe = $enPath.Source }
    }

    if (-not $exe) {
        Write-Host "ERROR: Ollama no esta instalado, o no esta donde se esperaba." -ForegroundColor Red
        Write-Host "  Se ha buscado en:"
        foreach ($c in $candidatos) { Write-Host "    $c" }
        Write-Host "  y en el PATH. Este script NO instala nada: instalalo tu y vuelve a ejecutarlo."
        exit 1
    }

    Write-Host "      Encontrado: $exe"
    if (-not (Test-Path $CarpetaLogs)) { New-Item -ItemType Directory -Path $CarpetaLogs | Out-Null }
    $marca = Get-Date -Format "yyyy-MM-dd_HHmmss"
    $logSalida = Join-Path $CarpetaLogs "ollama_$marca.log"
    $logError = Join-Path $CarpetaLogs "ollama_$marca.err.log"

    try {
        Start-Process -FilePath $exe -ArgumentList "serve" -WindowStyle Hidden `
            -RedirectStandardOutput $logSalida -RedirectStandardError $logError
    } catch {
        Write-Host "ERROR: no se ha podido lanzar Ollama." -ForegroundColor Red
        Write-Host "  Detalle: $($_.Exception.Message)"
        exit 1
    }

    Write-Host "      Arrancando en segundo plano. Registros en $CarpetaLogs"
    $version = $null
    foreach ($i in 1..$SegundosEspera) {
        Start-Sleep -Seconds 1
        $version = Test-Ollama
        if ($version) { break }
    }

    if ($version) {
        Write-Host "[2/3] Ollama respondiendo (version $version)." -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "ERROR: Ollama no ha respondido en $SegundosEspera segundos." -ForegroundColor Red
        Write-Host "  Que mirar, por este orden:"
        Write-Host "    1. El registro de errores: $logError"
        Write-Host "    2. Si el puerto 11434 lo esta ocupando otro programa."
        Write-Host "    3. Arrancarlo a mano en otra terminal para ver los mensajes:"
        Write-Host "         & `"$exe`" serve"
        Write-Host "  El asistente no se abre porque sin Ollama no puede redactar respuestas."
        Write-Host "  Para consultar solo los documentos, sin modelo, puedes usar:"
        Write-Host "         .\.venv\Scripts\python.exe consultar_documentos.py"
        exit 1
    }
}

# --- 4. Abrir el asistente con el Python del proyecto -----------------------
Write-Host "[3/3] Abriendo el asistente. Escribe /salir para terminar." -ForegroundColor Green
Write-Host ""

Push-Location $Proyecto
try {
    & $Python $Asistente
    $codigo = $LASTEXITCODE
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "Asistente cerrado. Ollama sigue activo para la proxima consulta."
Write-Host "Si quieres detenerlo: Get-Process ollama | Stop-Process"
exit $codigo
