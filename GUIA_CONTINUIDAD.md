# Continuidad y puesta en marcha — actualizada 2026-09-13

## Dónde está el proyecto
Carpeta original en F: C:\Users\Fer\Documents\Codex\2026-09-07\crear\outputs\interemprex-ia-local.
El Mac usa VS Code Remote SSH para editar y ejecutar ahí. La IA sigue en F. D aún no está configurado.

## Retomar cada día

Seis pasos. El último es el único comando que hay que escribir.

1. **Encender F** y dejarlo despierto. Iniciar sesión en Windows como `fer` y comprobar que Tailscale está conectado, tanto en F como en el cliente.
2. **Abrir VS Code en el Mac.**
3. **Conectar por Remote SSH** al alias `ordenador-f`. Confirmar que la ventana muestra `SSH: ordenador-f`.
4. **Abrir la carpeta original**: `C:\Users\Fer\Documents\Codex\2026-09-07\crear\outputs\interemprex-ia-local`.
5. **Abrir una terminal PowerShell remota** en VS Code. Es la terminal de F, no la del Mac.
6. **Ejecutar el arranque**:

```powershell
.\iniciar_asistente.ps1
```

Eso es todo. El script localiza el proyecto por sí mismo, comprueba que están el Python de `.venv` y el asistente, reutiliza Ollama si ya responde y lo arranca en segundo plano si no. Al salir del asistente con `/salir`, Ollama queda disponible para la siguiente vez.

Si algo falla, el script indica qué mirar. Los registros de diagnóstico de Ollama quedan en la carpeta `logs/` del proyecto.

### Si solo quieres consultar los documentos, sin modelo
```powershell
.\.venv\Scripts\python.exe consultar_documentos.py
```
No necesita Ollama.

### Copia de seguridad
```powershell
.\crear_copia_seguridad.ps1
```
Genera un ZIP fechado en `C:\Users\Fer\Documents\Copias-INTEREMPREX`, fuera del proyecto. Protege frente a cambios o borrados accidentales, **no frente a una avería de F**: está en el mismo disco.

### Lo que sigue sin estar resuelto
No hay que reinstalar Python ni volver a descargar el modelo. El arranque desatendido tras reiniciar Windows sigue pendiente: `iniciar_asistente.ps1` hay que lanzarlo a mano. No hay encendido remoto de F. **El acceso desde el ordenador D no está probado.** El acceso desde fuera de casa, tampoco.

## Qué contiene el código
- `iniciar_asistente.ps1`: arranque diario en un comando. Comprueba el entorno, reutiliza o arranca Ollama y abre el asistente.
- `crear_copia_seguridad.ps1`: genera el ZIP fechado de respaldo fuera del proyecto.
- `asistente_documental.py`: busca los fragmentos pertinentes y pide a qwen3:8b una respuesta apoyada solo en ellos. Muestra siempre la procedencia y el texto literal. Si entre los fragmentos hay un procedimiento pendiente de aprobación, no llama al modelo y entrega el texto original.
- `consultar_documentos.py`: solo búsqueda, sin modelo. Devuelve las secciones más parecidas con su procedencia y su texto literal.
- `probar_ollama.py`: una consulta suelta a la API, para comprobar que la cadena funciona.
- `chat_ollama.py`: chat de terminal con historial de sesión, anterior a la consulta documental. Se conserva.
- `comprobar_entorno.py`: identifica equipo e intérprete.

Todo con la biblioteca estándar de Python: no hay dependencias que instalar. `.venv` pertenece a F y se conserva allí; los modelos de Ollama están fuera del proyecto y no se copian.

## Claude y Codex

La primera tarea de Claude es leer el estado y confirmar si realmente puede acceder a la carpeta original de F. Una sesión web con adjuntos solo dispone de una instantánea. No convertir una carpeta temporal de Claude en el servidor del proyecto.

Claude Code debe trabajar sobre esta misma carpeta remota cuando su instalación y autenticación se hayan verificado. No asumir que una extensión instalada en Mac está instalada en F. Claude Code y Ollama tienen proveedores y autenticación independientes.

Antes de cada tarea: leer ESTADO_PROYECTO.md y las instrucciones. Al terminar: registrar cambios, archivos, evidencia, pendientes y siguiente paso. Un asistente edita y el otro revisa después. Si cambia el ejecutor, el usuario le entrega el estado actualizado. No hay sincronización automática entre chats.

Para Claude web, reemplazar la instantánea anterior por una nueva cuando cambie el proyecto. Para copias separadas de código, el repositorio privado interemprex/interemprex-ia-local ya está configurado; compartir cambios requiere commit, push y pull.

## Siguiente desarrollo propuesto
Crear un chat de terminal en Python que conserve mensajes durante la sesión, permita salir y controle el tamaño del historial. Explicar primero el concepto de lista de mensajes. Mantener el modelo y la API actuales. Memoria entre reinicios, documentos con fuentes, CRM y automatizaciones quedan para etapas posteriores.
