<#
    Copia de seguridad local del proyecto INTEREMPREX.

    Genera un ZIP fechado en una carpeta situada FUERA del proyecto, para que un
    borrado o un cambio accidental dentro de la carpeta de trabajo no se lleve
    tambien la copia.

    Se incluye por LISTA EXPLICITA, no por exclusion: solo entra lo que aparece
    nombrado abajo. Asi, si manana aparece un archivo con credenciales o con
    conversaciones, no se cuela en la copia por descuido.

    ATENCION: esta copia vive en el mismo disco que el proyecto. Protege frente a
    errores propios, NO frente a una averia del equipo F. Para eso hace falta
    otro soporte o un destino remoto.
#>

$ErrorActionPreference = "Stop"

$Proyecto = $PSScriptRoot
$Destino = Join-Path $env:USERPROFILE "Documents\Copias-INTEREMPREX"

# --- Lista explicita de lo que se copia -------------------------------------
$Codigo = @(
    "asistente_documental.py",
    "consultar_documentos.py",
    "chat_ollama.py",
    "probar_ollama.py",
    "comprobar_entorno.py",
    "iniciar_asistente.ps1",
    "crear_copia_seguridad.ps1",
    ".gitignore"
)
$Documentacion = @(
    "README.md",
    "CLAUDE.md",
    "AGENTS.md",
    "CONTEXTO_NEGOCIO.md",
    "ESTADO_PROYECTO.md",
    "GUIA_CONTINUIDAD.md",
    "TRASPASO_CLAUDE.md"
)
$Negocio = @(
    "data\documentos\01_presentacion_interemprex.md",
    "data\documentos\02_catalogo_servicios_interemprex.md",
    "data\documentos\03_proceso_trabajo_interemprex.md"
)

# Lo que NUNCA entra, y por que. Se enumera para dejar constancia.
$Excluido = @(
    ".venv            entorno virtual: se reconstruye, ocupa mucho y no es codigo propio",
    "modelos Ollama   viven fuera del proyecto y pesan gigabytes",
    "__pycache__      cache de Python, se regenera sola",
    "logs\            registros de diagnostico de Ollama",
    "data\asistente\  registros de conversaciones con el modelo",
    "data\consultas\  registros de busquedas",
    "data\pruebas\    evidencias de pruebas, incluyen respuestas del modelo",
    "credenciales     no hay ninguna en el arbol; la lista explicita lo garantiza"
)

Write-Host ""
Write-Host "Copia de seguridad de INTEREMPREX" -ForegroundColor Cyan
Write-Host "Proyecto: $Proyecto"
Write-Host "Destino : $Destino"
Write-Host ""

if (-not (Test-Path $Destino)) {
    New-Item -ItemType Directory -Path $Destino -Force | Out-Null
    Write-Host "Carpeta de copias creada."
}

$marca = Get-Date -Format "yyyy-MM-dd_HHmm"
$nombreZip = "copia_interemprex-ia-local_$marca.zip"
$rutaZip = Join-Path $Destino $nombreZip
$temporal = Join-Path $env:TEMP "copia_interemprex_$marca"

if (Test-Path $temporal) { Remove-Item $temporal -Recurse -Force }
New-Item -ItemType Directory -Path $temporal -Force | Out-Null

# --- Copiar respetando la estructura de carpetas ----------------------------
$copiados = @()
$faltan = @()
foreach ($rel in ($Codigo + $Documentacion + $Negocio)) {
    $origen = Join-Path $Proyecto $rel
    if (-not (Test-Path $origen)) {
        $faltan += $rel
        continue
    }
    $destinoArchivo = Join-Path $temporal $rel
    $carpetaPadre = Split-Path $destinoArchivo -Parent
    if (-not (Test-Path $carpetaPadre)) { New-Item -ItemType Directory -Path $carpetaPadre -Force | Out-Null }
    Copy-Item $origen $destinoArchivo
    $tam = (Get-Item $origen).Length
    $copiados += [PSCustomObject]@{ Archivo = $rel; Bytes = $tam }
}

if ($faltan.Count -gt 0) {
    Write-Host "AVISO: estos archivos de la lista no existen y no se han copiado:" -ForegroundColor Yellow
    foreach ($f in $faltan) { Write-Host "  $f" }
    Write-Host ""
}

# --- Inventario dentro del propio ZIP ---------------------------------------
$inventario = @()
$inventario += "INVENTARIO DE LA COPIA"
$inventario += "Proyecto : INTEREMPREX - asistente documental local"
$inventario += "Origen   : $Proyecto"
$inventario += "Equipo   : $env:COMPUTERNAME"
$inventario += "Fecha    : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$inventario += ""
$inventario += "ARCHIVOS INCLUIDOS ($($copiados.Count))"
foreach ($c in $copiados) {
    $inventario += ("  {0,-60} {1,8} bytes" -f $c.Archivo, $c.Bytes)
}
$inventario += ""
$inventario += "EXCLUIDO DELIBERADAMENTE"
foreach ($e in $Excluido) { $inventario += "  $e" }
$inventario += ""
$inventario += "ALCANCE DE ESTA COPIA"
$inventario += "  Protege frente a cambios o borrados accidentales dentro del proyecto."
$inventario += "  NO protege frente a una averia del equipo F: vive en el mismo disco."
$inventario += "  Para eso hace falta otro soporte o un destino remoto."
$inventario += ""
$inventario += "PARA RESTAURAR"
$inventario += "  Descomprimir y copiar los archivos sobre la carpeta del proyecto."
$inventario += "  El entorno virtual .venv NO esta en la copia: se recrea aparte."

$rutaInventario = Join-Path $temporal "INVENTARIO.txt"
$inventario | Out-File -FilePath $rutaInventario -Encoding utf8

# --- Comprimir y comprobar --------------------------------------------------
Compress-Archive -Path (Join-Path $temporal "*") -DestinationPath $rutaZip -Force
Remove-Item $temporal -Recurse -Force

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($rutaZip)
$entradas = $zip.Entries | ForEach-Object { $_.FullName }
$zip.Dispose()

$esperados = ($Codigo + $Documentacion + $Negocio | Where-Object { $faltan -notcontains $_ }).Count + 1
Write-Host "ZIP creado: $rutaZip"
Write-Host "Tamano    : $([math]::Round((Get-Item $rutaZip).Length / 1KB, 1)) KB"
Write-Host "Entradas  : $($entradas.Count) (esperadas $esperados, incluido INVENTARIO.txt)"
Write-Host ""

$problemas = @()
if ($entradas.Count -ne $esperados) { $problemas += "el numero de entradas no coincide" }
foreach ($patron in @(".venv", "__pycache__", "data/asistente", "data/consultas", "data/pruebas", "logs/")) {
    if ($entradas -match [regex]::Escape($patron)) { $problemas += "se ha colado algo excluido: $patron" }
}
if ($problemas.Count -gt 0) {
    Write-Host "REVISAR:" -ForegroundColor Red
    foreach ($p in $problemas) { Write-Host "  $p" }
    exit 1
}

Write-Host "Comprobado: el ZIP se abre y contiene lo previsto, sin material excluido." -ForegroundColor Green
Write-Host ""
Write-Host "Recuerda: esta copia esta en el mismo disco que el proyecto. Protege frente a"
Write-Host "errores propios, no frente a una averia de F."
exit 0
