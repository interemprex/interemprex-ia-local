# Continuidad y puesta en marcha — 2026-09-10

## Dónde está el proyecto
Carpeta original en F: C:\Users\Fer\Documents\Codex\2026-09-07\crear\outputs\interemprex-ia-local.
El Mac usa VS Code Remote SSH para editar y ejecutar ahí. La IA sigue en F. D aún no está configurado.

## Retomar cada día
1. Encender F, mantenerlo despierto y conectado. Para este procedimiento manual, iniciar sesión Windows como fer. Tailscale debe estar conectado también en el cliente.
2. En VS Code del Mac, conectar por Remote SSH al alias ordenador-f y abrir la carpeta original. Confirmar SSH: ordenador-f en la ventana.
3. En la terminal PowerShell remota, comprobar si Ollama ya responde:
```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/version' -TimeoutSec 10
```
4. Si devuelve una versión, reutilizar el servidor. Si hay conexión rechazada, iniciar en esa terminal:
```powershell
$env:OLLAMA_HOST = '127.0.0.1:11434'
& 'C:\Users\Fer\AppData\Local\Programs\Ollama\ollama.exe' serve
```
Si aparece otro error, revisarlo antes de iniciar más procesos. Esta terminal muestra registros y queda ocupada por el servidor.
5. En una segunda terminal PowerShell remota, dentro de la carpeta original:
```powershell
.\.venv\Scripts\python.exe comprobar_entorno.py
.\.venv\Scripts\python.exe probar_ollama.py
```
Se espera equipo DESKTOP-T6C436J, Python de .venv, entorno virtual True y respuesta en español. No hace falta activar .venv cuando se utiliza la ruta del ejecutable.

No reinstalar Python ni volver a descargar el modelo cada día. Mantener la terminal del servidor abierta durante las pruebas. El arranque desatendido, comportamiento tras reinicio y acceso desde otra red todavía requieren configuración o prueba. No hay encendido remoto configurado.

## Qué contiene el código
- comprobar_entorno.py: identifica equipo e intérprete.
- probar_ollama.py: una consulta por ejecución, API /api/chat, modelo qwen3:8b, think=False, stream=False, contexto 4096, máximo 256 tokens generados, espera de hasta 180 segundos. Solo biblioteca estándar; no hay dependencias adicionales que instalar.
- .venv pertenece a F y se conserva allí; los modelos están fuera del proyecto. El paquete de traspaso contiene código y documentación, no el entorno ejecutable completo.

## Claude y Codex
La primera tarea de Claude es leer el estado y confirmar si realmente puede acceder a la carpeta original de F. Una sesión web con adjuntos solo dispone de una instantánea. No convertir una carpeta temporal de Claude en el servidor del proyecto.

Claude Code debe trabajar sobre esta misma carpeta remota cuando su instalación y autenticación se hayan verificado. No asumir que una extensión instalada en Mac está instalada en F. Claude Code y Ollama tienen proveedores y autenticación independientes.

Antes de cada tarea: leer ESTADO_PROYECTO.md y las instrucciones. Al terminar: registrar cambios, archivos, evidencia, pendientes y siguiente paso. Un asistente edita y el otro revisa después. Si cambia el ejecutor, el usuario le entrega el estado actualizado. No hay sincronización automática entre chats.

Para Claude web, reemplazar la instantánea anterior por una nueva cuando cambie el proyecto. Para copias separadas de código, configurar GitHub privado y compartir commits cuando llegue ese paso; hoy GitHub no está verificado.

## Siguiente desarrollo propuesto
Crear un chat de terminal en Python que conserve mensajes durante la sesión, permita salir y controle el tamaño del historial. Explicar primero el concepto de lista de mensajes. Mantener el modelo y la API actuales. Memoria entre reinicios, documentos con fuentes, CRM y automatizaciones quedan para etapas posteriores.
