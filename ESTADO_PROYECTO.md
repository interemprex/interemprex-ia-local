# Estado del proyecto — 2026-09-13

Responsable de esta actualización: Codex. Referencia actual para ambos asistentes. Este documento sustituye las notas de estado antiguas del README.

## Objetivo
Objetivo empresarial confirmado por el usuario el 2026-09-13: INTEREMPREX tiene como objetivo desarrollar aplicaciones a medida para negocios y encargarse de su mantenimiento, incluyendo desarrollo web, automatización e internacionalización. La referencia empresarial vigente es `CONTEXTO_NEGOCIO.md`; sustituye las descripciones anteriores de agencia digital genérica. Tarifas, entregables y condiciones todavía requieren definición y aprobación.

Aprender IA y programación construyendo un asistente documental local para INTEREMPREX con fuentes. Después incorporar RAG, CRM, LeadFinder y herramientas. Preparar Claude, Claude Code, GitHub, Python, VS Code y Ollama. Avanzar en pasos pequeños, explicando propósito y comprobación.

## Arquitectura
MacBook Pro → Tailscale → OpenSSH → VS Code remoto → Python y Ollama en F. La consulta Python a qwen3:8b funciona. Ordenador D se incorporará como otro cliente. El acceso desde fuera de casa está previsto, pero aún no se ha probado.

Directorio de F: `C:\Users\Fer\Documents\Codex\2026-09-07\crear\outputs\interemprex-ia-local`.

## Equipos
- F: usuario fer, nombre Windows DESKTOP-T6C436J; Windows 11 25H2, build 26200.9168. La referencia inicial a Windows 10 estaba desactualizada; edición exacta actual pendiente. CPU Ryzen 9 9900X3D, GPU RTX 5080: verificados. nvidia-smi reportó 16303 MiB y controlador 616.56.
- F según historial: RAM 64 GB, SSD BIWIN NV3500 2 TB y MSI PRO X870E-P WIFI; estos tres datos no se han verificado directamente en esta sesión.
- MacBook Pro: cliente actual, usuario dario, macOS 26.5.2 según captura de Tailscale. No aloja el modelo.
- D: Windows 11 Pro build 26200, i7-8700K, 16 GB RAM y MSI Z370 GAMING M5 según captura histórica. RTX 3060 12 GB según conversación anterior. Todavía no conectado.

## Completado y comprobado mediante resultados/capturas
1. Tailscale 1.102.3 en F y Mac, ambos Connected. F: ordenador-f / 100.86.251.101. Mac: 100.120.229.23.
2. OpenSSH Server en F instalado sin necesidad de reiniciar. Servicio sshd Running / Automatic.
3. Regla OpenSSH-Server-In-TCP: LocalAddress 100.86.251.101, InterfaceAlias Tailscale, RemoteAddress Any. No limitada aún a un cliente. Esto describe esa regla; no constituye auditoría de todo el firewall.
4. Prueba nc desde Mac al puerto 22 de F: succeeded.
5. Clave Ed25519 del Mac creada en /Users/dario/.ssh/interemprex_f; pública en .pub. Privada permanece en Mac; no subirla ni copiarla al repositorio.
6. Cuenta fer administradora; pública añadida a C:\ProgramData\ssh\administrators_authorized_keys. icacls completó correctamente la eliminación de herencia y concesión a Administradores y SYSTEM.
7. SSH con clave desde Mac a fer@100.86.251.101: acceso correcto. Huella Ed25519 de F observada en ambas máquinas: SHA256:whBhU13v/4x3yIXDaPnmA2fwsYwd47Nj0zEm9twngvc.
8. VS Code del Mac conectado a SSH: ordenador-f, carpeta de proyecto abierta.
9. Terminal remota: whoami = desktop-t6c436j\fer; hostname = DESKTOP-T6C436J; Git 2.55.0.windows.5.
10. Python 3.13.15 x64 instalado para fer por WinGet. Base: C:\Users\Fer\AppData\Local\Programs\Python\Python313\python.exe.
11. .venv creado en la raíz. pip 26.2.1 dentro del entorno. Extensión Python Microsoft habilitada en SSH: ordenador-f.
12. comprobar_entorno.py ejecutado desde el editor: equipo F, ejecutable .venv\Scripts\python.exe, Entorno virtual True. Prefijo (.venv) visible en terminal.

## Configuración SSH en Mac
Archivo /Users/dario/.ssh/config:
```sshconfig
Host ordenador-f
    HostName 100.86.251.101
    User fer
    IdentityFile ~/.ssh/interemprex_f
    IdentitiesOnly yes
    PasswordAuthentication no
    HostKeyAlgorithms ssh-ed25519
    ServerAliveInterval 30
    ServerAliveCountMax 3
```
PasswordAuthentication no está fijado en el cliente. No afirmar que se haya desactivado en el servidor.

## Situación de componentes y pendientes
- Ollama instalado y probado: versión 0.33.3, API local, qwen3:8b y ejecución en GPU verificados por capturas. Integración Python verificada el 10 de septiembre; detalles al final.
- GitHub: SUPERADO el 12 de septiembre de 2026. Repositorio privado creado, remoto conectado y primer commit publicado. Ver la sección final.
- Claude Code de Anthropic aparece en «SSH: ORDENADOR-F - INSTALLED». Según la respuesta de Claude Code compartida por el usuario, la sesión funciona y ejecutó una comprobación de hostname y carpeta, además de leer los archivos originales. Acceso operativo de lectura reportado; no se ha probado escritura ni se ha inspeccionado el método de autenticación.
- Claude: archivos del traspaso visibles en Contexto del proyecto «IA L» según captura del usuario. Su respuesta posterior, compartida como texto, resume el estado correctamente y reconoce disponer únicamente de copias. Traspaso documental recibido; acceso de Claude Code a la carpeta original aún no verificado.
- Inicio de Ollama sin sesión interactiva, disponibilidad tras reinicio, suspensión y acceso desde otra red pendientes. F debe estar encendido y conectado; no se ha configurado encendido remoto.
- Incorporar D posteriormente.

## Procedimiento histórico de instalación (ya superado)
La instalación ya terminó según captura. NO repetir la instalación propuesta a continuación salvo diagnóstico que lo justifique. Comando de instalación anteriormente propuesto (histórico):
```powershell
winget install --id Ollama.Ollama --exact --source winget --scope user --silent
```
Verificación histórica ya completada: ejecutable localizado y versión 0.33.3 comprobada. Comando de referencia:
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
```
Verificar servidor local antes de descargar modelo. Mantener API en loopback de F. Python remoto usa localhost de F. No publicar 11434 en Internet.

## Registro de coordinación
- 2026-09-09 / Codex: consolidación del progreso y traspaso. Sin instalación de componentes durante esta actualización.
- Próximo ejecutor propuesto: Claude Code cuando disponga de acceso a F. Codex puede revisar después. Un solo asistente edita la carpeta a la vez.
- Añadir entradas con fecha, asistente, equipo, cambio, archivos, pruebas, pendientes y siguiente paso; incluir commit cuando exista. No hay commit verificado todavía.


## Comprobación del 10 de septiembre de 2026 — Codex
- El usuario retoma Ollama. Ejecutable localizado en C:\Users\Fer\AppData\Local\Programs\Ollama\ollama.exe.
- La consulta desde el entorno de Codex a 127.0.0.1:11434/api/version devolvió conexión rechazada.
- La ejecución de ollama.exe desde el entorno restringido de Codex devolvió Acceso denegado. No se ha modificado la instalación ni iniciado un servidor con la cuenta del entorno restringido.
- Paso propuesto entonces, ya completado por el usuario: iniciar ollama serve desde la terminal remota de fer, consultar la API, descargar y probar el modelo.

## Estado vigente de Ollama — 10 de septiembre de 2026
Esta sección actualiza y deja superadas las comprobaciones anteriores de servidor/modelo pendientes.
- Ollama 0.33.3: API /api/version respondió correctamente según captura.
- Servidor manual en terminal de fer, escuchando en 127.0.0.1:11434.
- RTX 5080 detectada por CUDA. Aviso de AMD corresponde a la gráfica integrada descartada.
- qwen3:8b descargado con success (5.2 GB).
- Primera inferencia por CLI produjo una respuesta en español.
- ollama ps: qwen3:8b, ID 500a1f067a9f, 5.6 GB, PROCESSOR 100% GPU, contexto 4096. Evidencia: captura del usuario.
- Codex creó probar_ollama.py: primera consulta a /api/chat con biblioteca estándar, sin paquetes adicionales, think=False, contexto 4096. No tiene RAG ni memoria persistente.
- La ejecución desde el entorno restringido de Codex fue denegada por permisos. Posteriormente el usuario ejecutó .\.venv\Scripts\python.exe probar_ollama.py desde VS Code remoto como fer: la captura confirma equipo DESKTOP-T6C436J, intérprete de .venv, respuesta en español y regreso al indicador de PowerShell sin error visible. Integración Python -> API local de Ollama -> qwen3:8b verificada por esta evidencia.
- 2026-09-10 / Codex: actualización de este archivo tras comprobar la captura. Sin cambios de código ni de configuración en este paso.
- Siguiente paso propuesto: preparar un chat interactivo en Python con historial durante la sesión. El arranque persistente tras reinicio sigue pendiente; actualmente mantener abierta la terminal de ollama serve.

## Traspaso solicitado a Claude — 10 de septiembre de 2026
- El usuario pide continuar el proyecto actualizado con Claude. Codex preparó documentación y un paquete de código/contexto. Una captura posterior muestra los archivos cargados en Contexto del proyecto «IA L» de Claude. Esto verifica la carga visible, no una sincronización automática ni acceso a F.
- README.md y TRASPASO_CLAUDE.md actualizados; GUIA_CONTINUIDAD.md añadida con arranque diario y protocolo de coordinación.
- Paquete exportado en outputs/traspaso-claude-2026-09-10: texto consolidado para adjuntar y ZIP con archivos fuente seleccionados. Excluye .venv, modelos, claves, credenciales y capturas. Es una instantánea operativa, no una transcripción literal del chat.
- Próximo paso inmediato: Claude lee el paquete, confirma estado y acceso real a F. Después retoma el chat interactivo propuesto, en pasos pequeños. Codex deja de editar al concluir este traspaso.
- Continuación solicitada al propio Codex: revisión del estado y guía para verificar Claude Code desde la ventana de VS Code Remote SSH en F. Se actualizaron únicamente estas notas; sin instalaciones ni modificaciones del código. Pendiente que el usuario compruebe la extensión en SSH: ordenador-f, autenticación y lectura de los archivos originales por Claude Code.
- Revisión de respuesta de Claude web: confirma recepción y comprensión del contexto. Su propuesta de comprobar PATH, ~/.local/bin y WinGet no descarta una instalación de la extensión de VS Code con CLI incluido. Antes de instalar otra copia, comprobar Claude Code de Anthropic en la ventana SSH: ordenador-f. Sin nuevas pruebas de instalación o autenticación y sin cambios de código.
- Captura posterior: Claude Code de Anthropic está listado en SSH: ORDENADOR-F - INSTALLED, con icono visible en el editor. Siguiente paso: abrir el panel, autenticar si se solicita y comprobar lectura de la carpeta original mediante herramientas. No reinstalar por falta de un comando en PATH.
- Preferencia del usuario incorporada a CLAUDE.md: avisar antes de fases de especial esfuerzo recomendando un modelo avanzado y explicar el motivo. Actualización documental únicamente; los adjuntos anteriores de Claude web no se actualizan automáticamente.
- Verificación de acceso compartida por el usuario: Claude Code informó ejecución en DESKTOP-T6C436J, carpeta C:\Users\Fer\Documents\Codex\2026-09-07\crear\outputs\interemprex-ia-local y lectura del modelo qwen3:8b y URL http://127.0.0.1:11434/api/chat de probar_ollama.py. También resumió las reglas y el estado. Evidencia: respuesta textual de Claude Code pegada por el usuario; no es una ejecución independiente de Codex.
- Traspaso operativo listo para continuar en Claude Code. No se han probado escrituras de Claude Code. Codex actualizó únicamente este estado y pasa a revisión; Claude Code será el único editor durante su siguiente tarea. Siguiente desarrollo propuesto: chat Python con historial limitado durante la sesión, salida y manejo de errores, conservando la API y el modelo actuales.

## Chat interactivo — 10 de septiembre de 2026 — Claude Code (Opus 5) en F

Claude Code pasa a ser el único editor del árbol. Todos los comandos de esta sección se ejecutaron en F (DESKTOP-T6C436J), no en Mac ni en D.

### Verificación de acceso
- Claude Code lee la carpeta original mediante herramientas: hostname DESKTOP-T6C436J y ruta `C:\Users\Fer\Documents\Codex\2026-09-07\crear\outputs\interemprex-ia-local`. Queda resuelto el punto pendiente del traspaso.
- `.venv\Scripts\python.exe` responde: Python 3.13.15 en F.

### Estado del servidor al empezar
- Al iniciar la sesión NO había servidor activo: `/api/version` devolvió WinError 10061 y no existía ningún proceso `ollama`. Confirma que el arranque persistente sigue pendiente.
- Claude Code lanzó `ollama serve` en segundo plano en F. La API respondió a los 2 s con versión 0.33.3. Este proceso quedó en ejecución al cerrar el paso; no es un servicio, desaparecerá al reiniciar.
- `/api/tags`: qwen3:8b presente (5225388164 bytes).
- `ollama ps` tras las pruebas: qwen3:8b, ID 500a1f067a9f, 5.6 GB, PROCESSOR 100% GPU, CONTEXT 4096.

### Archivo nuevo: chat_ollama.py
AVISO: la descripción de `recortar()` y del límite de esta subsección quedó SUPERADA por la corrección del mismo día, más abajo. Se conserva como registro de lo que se hizo primero.

Chat de terminal contra `127.0.0.1:11434/api/chat` (localhost de F). Solo biblioteca estándar, sin paquetes nuevos, mismo estilo que probar_ollama.py. `stream: False` y `think: False`; `num_ctx` 4096 y `num_predict` 512.
- Historial en memoria durante la sesión, en la lista `historial`. No hay persistencia en disco: al salir se pierde.
- Límite de tamaño: `MAX_INTERCAMBIOS = 8`. `recortar()` conserva siempre el mensaje de sistema y como mucho los 16 mensajes más recientes.
- Salida: `/salir`, `salir`, `/exit`, `exit`, `/quit`, `quit`, Ctrl+C y Ctrl+D. `/limpiar` reinicia el historial sin cerrar el programa.
- El turno solo se guarda cuando la respuesta llega correctamente, para no dejar un mensaje de usuario sin respuesta en el historial.

### Pruebas ejecutadas y resultado real
1. Servidor apagado, entrada `hola que tal`: imprimió "Sin respuesta de Ollama. Comprueba que 'ollama serve' sigue activo en F." con el detalle WinError 10061. El programa NO se cerró; siguió aceptando entrada y salió con `/salir`. Gestión de errores de conexión verificada.
2. `recortar()` con 30 mensajes más el de sistema: devolvió 17 elementos, el primero `system` y el último el más reciente. Límite verificado.
3. Dos turnos encadenados con servidor activo: "Me llamo Fer y trabajo en INTEREMPREX" y después "sin volver a leer nada más: ¿cómo me llamo?". El modelo respondió "Te llamas Fer." Historial de sesión verificado.
4. `/limpiar` seguido de la misma pregunta: el modelo respondió "No sé tu nombre." Borrado del historial verificado.
5. `probar_ollama.py` conservado sin cambios y ejecutado de nuevo: respondió correctamente. No hay regresión.

### Pendientes tras este paso
- Sin persistencia entre sesiones, sin RAG y sin fuentes documentales. El chat no conoce documentos de INTEREMPREX.
- Sin streaming: la respuesta aparece de golpe tras "Pensando...".
- Arranque persistente de Ollama tras reinicio o suspensión: sigue pendiente. Hoy hay que lanzar `ollama serve` a mano.
- GitHub sigue sin repositorio, remoto ni commits.
- Siguiente paso propuesto: elegir entre añadir streaming al chat (mejora de uso, cambio pequeño) o empezar la ingesta documental con fuentes, que es el objetivo inicial. La ingesta documental sí requiere un modelo avanzado de IA por el diseño de troceado, almacenamiento e citación de fuentes.

## Corrección del historial y control de tamaño — 10 de septiembre de 2026 — Claude Code (Opus 5) en F

El usuario detectó un defecto en la primera versión y pidió corregirlo antes de añadir funcionalidades. Todo ejecutado en F (DESKTOP-T6C436J). Claude Code sigue como único editor. `probar_ollama.py` no se ha tocado.

### Defecto confirmado y reproducido
`recortar()` recibía los pares completos MÁS la pregunta pendiente, es decir una lista de longitud impar, y se quedaba con los últimos 16 elementos. Al cortar por una posición par eliminaba la pregunta más antigua pero conservaba su respuesta: la conversación enviada empezaba por un mensaje `assistant` huérfano y a partir de ahí los papeles quedaban invertidos.

Reproducido con la función antigua y 12 intercambios más una pregunta: el primer mensaje tras `system` era `respuesta 5`, y la comprobación de alternancia devolvió 17 fallos. No era una hipótesis.

### Qué se ha cambiado
- `recortar()` se sustituye por `preparar_peticion(completos, pregunta)`. Recibe por separado los intercambios ya cerrados y la pregunta pendiente, de modo que nunca puede partir un par por la mitad. Descarta de dos en dos, siempre intercambios enteros.
- Definición explícita del límite, antes ambigua: **`MAX_INTERCAMBIOS = 8` incluye el turno actual**. Viajan como mucho 7 intercambios previos más la pregunta. Se indica en el mensaje de arranque del programa.
- El historial completo de la sesión se conserva en memoria; los límites se aplican solo al construir cada petición. Así una pregunta larga puntual no borra permanentemente la conversación.
- Control de tamaño: `PRESUPUESTO_ENTRADA = NUM_CTX - NUM_PREDICT - MARGEN_TOKENS` = 4096 - 512 - 128 = 3456 tokens estimados. Reserva explícita para la respuesta, más margen para la plantilla de chat que añade Ollama.
- Preguntas demasiado largas: si la pregunta no cabe ni siquiera sola con el mensaje de sistema, se rechaza antes de enviarla, indicando cuántos tokens y caracteres sobran. El programa continúa y la pregunta rechazada NO entra en el historial.
- Si la pregunta cabe pero el historial no, se sueltan intercambios completos, del más antiguo al más reciente, hasta entrar en el presupuesto.
- Cada turno imprime `[contexto: N intercambios previos, ~M tokens estimados]`, para que el recorte sea visible en lugar de silencioso.

### Sobre la estimación de tokens: es una estimación, no un recuento
`estimar_tokens()` aproxima 3,5 caracteres por token en texto corriente y cobra un token por cada carácter que no sea letra ni espacio. No usa el tokenizador real, que vive dentro de Ollama.

Se midió el error real contra `prompt_eval_count` devuelto por la API, con qwen3:8b. Primera versión, que solo dividía por 3,5:

| caso | caracteres | estimado | real | error |
|---|---|---|---|---|
| prosa española | 4720 | 1378 | 1043 | +32% |
| cifras | 2287 | 683 | 2329 | **-71%** |
| código | 1980 | 595 | 762 | -22% |
| URLs | 2600 | 772 | 843 | -8% |
| frase corta | 36 | 40 | 52 | -23% |

La subestimación del 71% con cifras era un riesgo real de desbordar el contexto, así que se corrigió la fórmula. Medición tras el cambio:

| caso | caracteres | estimado | real | error |
|---|---|---|---|---|
| prosa española | 4720 | 1409 | 1043 | +35% |
| cifras | 2287 | 1891 | 2329 | -19% |
| código | 1980 | 812 | 762 | +7% |
| URLs | 2600 | 1174 | 843 | +39% |
| frase corta | 36 | 43 | 52 | -17% |

Conclusión honesta: sigue siendo aproximada. Sobra margen con texto normal y falta hasta un 19% con cifras. Si se queda corta, Ollama recorta el principio del prompt por su cuenta y el chat pierde memoria sin avisar. `MARGEN_TOKENS` existe por eso. Un recuento exacto exigiría el tokenizador del modelo, que hoy no está expuesto sin añadir dependencias.

### Pruebas ejecutadas y resultado real
1. Estructura, de 0 a 12 intercambios previos: en los 13 casos la petición empieza por `system`, sigue con `user`, alterna correctamente y termina en la pregunta pendiente. Con 8 o más previos envía siempre 7 y 16 mensajes, y la ventana avanza (`pregunta 2`, `pregunta 3`, … `pregunta 6`). Cero fallos.
2. Flujo real con 10 turnos y modelo activo. La línea de contexto progresó 0,1,2,3,4,5,6,7,7,7. En el turno 1 se plantó la palabra TORNILLO y en el turno 9 MARTILLO. Al preguntar en el turno 10 qué palabras clave aparecían, el modelo respondió: 3, 4, 5, 6, 7, 8 y MARTILLO. Es decir, recordó exactamente los turnos 3 a 9 y perdió los turnos 1 y 2. La ventana de 7 previos se comporta como está documentada.
3. Pregunta de 20 000 caracteres: rechazada con "sobran ~2288 tokens estimados (~8008 caracteres)". El programa siguió y el turno siguiente mostró `1 intercambios previos`, confirmando que la pregunta rechazada no se guardó.
4. Recorte por tamaño con modelo activo: tres preguntas de 4034 caracteres y una final de 2036. Pese a haber 2 y 3 intercambios disponibles, envió 1 y 2 respectivamente, quedando en 2342 y 2932 tokens estimados, por debajo de 3456. El límite de tamaño actuó antes que el de turnos.
5. Historial de 30 intercambios grandes: envió 6 y no 7, respetando ambos límites, sin fallos de estructura.
6. Regresión: `/limpiar`, `/salir` y memoria de un turno a otro siguen bien. `probar_ollama.py` reejecutado sin cambios: correcto.

Las pruebas 1 y 5 usan un script de comprobación que vive en la carpeta temporal de la sesión, fuera del repositorio, porque aún no hay decisión sobre dónde colocar pruebas en el proyecto.

### Pendientes tras esta corrección
- Sigue sin persistencia entre sesiones, sin RAG y sin fuentes documentales.
- Sigue sin streaming.
- El historial completo crece en memoria durante la sesión. Es texto y la sesión es corta, pero no está acotado.
- La estimación de tokens no es exacta; ver tabla anterior.
- Falta decidir dónde guardar pruebas automáticas dentro del repositorio.
- Arranque persistente de Ollama: sigue pendiente. GitHub: resuelto el 12 de septiembre de 2026, ver la sección final.

## Repositorio Git y publicación en GitHub — 12 de septiembre de 2026 — Claude Code (Opus 5) en F

Todo ejecutado en F (DESKTOP-T6C436J). Claude Code sigue como único editor. No se ha tocado `chat_ollama.py` ni `probar_ollama.py`, ni se ha reinstalado ningún componente existente.

### Situación de partida
- No existía repositorio: `git rev-parse --show-toplevel` devolvió *not a git repository*, ni en la carpeta ni en ninguna superior.
- `.gitignore` ya existía y cubría `.venv/`, `venv/`, `__pycache__/`, `.env`, `data/`, `models/`, `logs/`, `*.gguf`, `*.safetensors`, `*.pem`, `*.key`.
- Barrido de secretos sobre los archivos candidatos: sin claves privadas ni tokens. Los únicos aciertos fueron falsos positivos (`PasswordAuthentication no`, que es una directiva de configuración, y las constantes del estimador de tokens).

### Incidencia de permisos encontrada
La carpeta del proyecto pertenece a la cuenta `DESKTOP-T6C436J\CodexSandboxOffline` (SID terminado en 1003), no a `fer` (terminado en 1001). Es un resto del entorno restringido de Codex. Git lo rechazó con *dubious ownership* y se negó a operar.

Resuelto con la excepción que el propio Git recomienda, autorizada expresamente por el usuario: `git config --global --add safe.directory C:/Users/Fer/Documents/Codex/2026-09-07/crear/outputs/interemprex-ia-local`. **La causa real no está corregida**: el propietario de la carpeta sigue siendo la cuenta del sandbox. Si algún día se clona o se mueve el proyecto, puede reaparecer.

### Repositorio local
- `git init -b main`. Rama `main` desde el principio, sin renombrar.
- Identidad del autor: **ya existía** en la configuración global, `dbenitezc68-beep <dbenitezc68@gmail.com>`. No se inventó ni se modificó.
- Archivos incluidos, 10: `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `ESTADO_PROYECTO.md`, `GUIA_CONTINUIDAD.md`, `README.md`, `TRASPASO_CLAUDE.md`, `chat_ollama.py`, `comprobar_entorno.py`, `probar_ollama.py`.
- Excluidos y confirmados como ignorados: `.venv/` y `__pycache__/`. No hay modelos, credenciales ni documentos privados dentro del árbol.
- `README.md` reescrito: programas, uso del chat, explicación del historial y una sección explícita de limitaciones (sin memoria entre sesiones, sin RAG ni fuentes, olvido dentro de la sesión, estimación de tokens aproximada, sin streaming, Ollama no arranca solo).
- Primer commit: `b48e5ead2f185a4832be3af7556858aabfec1ace` (`b48e5ea`), 10 archivos, 594 inserciones.

### Autenticación de GitHub
- No existía ninguna: sin `gh`, sin `credential.helper` configurado, `fer` sin `~/.ssh` en F y `ssh -T git@github.com` respondió *Permission denied (publickey)*.
- Se instaló GitHub CLI 2.100.0 con `winget --scope user`, previa autorización del usuario. Es un componente **nuevo**, no una reinstalación. Ruta: `C:\Users\Fer\AppData\Local\Microsoft\WinGet\Packages\GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe\bin\gh.exe`. Aviso práctico: no está en el PATH de las terminales ya abiertas.
- `gh auth login` lo ejecutó **el usuario**, porque es interactivo y la sesión de Claude Code no lo es. Se eligió el flujo de código de dispositivo para poder autorizar desde el navegador del Mac.
- Verificado después por Claude Code, no dado por bueno: cuenta activa `interemprex`, tipo `User`, protocolo `https`, scopes `gist`, `read:org`, `repo`, `workflow`.
- **Detalle que conviene recordar**: la cuenta de GitHub es `interemprex`, pero los commits se firman con `dbenitezc68-beep <dbenitezc68@gmail.com>`. No es un error, pero autor y titular de la cuenta no coinciden.

### Creación y publicación
- Se comprobó primero que el nombre estuviera libre: `gh repo view interemprex/interemprex-ia-local` devolvió *Could not resolve to a Repository*, y `gh repo list interemprex` no devolvió ninguno. La cuenta no tenía repositorios. No se vinculó nada ajeno.
- Creado **privado y vacío**, y verificada la privacidad **antes** de subir nada: `isPrivate: true`, `visibility: PRIVATE`, `isEmpty: true`.
- Remoto `origin` por HTTPS y `git push -u origin main`.

### Verificación posterior a la publicación
| Comprobación | Resultado |
|---|---|
| URL | https://github.com/interemprex/interemprex-ia-local |
| Privacidad | `isPrivate: true`, `visibility: PRIVATE` |
| Rama por defecto | `main` |
| HEAD local | `b48e5ead2f185a4832be3af7556858aabfec1ace` |
| HEAD remoto (`git ls-remote`) | `b48e5ead2f185a4832be3af7556858aabfec1ace` — idéntico |
| Commits locales sin publicar | 0 |
| `git status -sb` | `## main...origin/main`, sin divergencia |
| Contenido remoto | los 10 archivos previstos; ni `.venv` ni `__pycache__` |

### Correcciones documentales derivadas
Cuatro afirmaciones quedaron falsas al crear el repositorio y se corrigieron: `AGENTS.md` («GitHub requiere configuración pendiente»), `GUIA_CONTINUIDAD.md` («hoy GitHub no está verificado»), y en este archivo las líneas de pendientes sobre GitHub. `README.md` incorpora ahora la URL del repositorio privado.

### Pendientes tras este paso
- El propietario de la carpeta sigue siendo `CodexSandboxOffline`. La excepción `safe.directory` tapa el síntoma, no la causa.
- Este archivo contiene IPs de Tailscale (100.86.251.101, 100.120.229.23) y la huella SSH pública de F. En un repositorio **privado** es aceptable y no son secretos, pero habría que revisarlo antes de hacerlo público alguna vez.
- No hay ramas de trabajo ni flujo de pull request: se trabaja directamente sobre `main`.
- `gh` no está en el PATH de terminales abiertas antes de su instalación.
- Sin cambios en lo demás: arranque persistente de Ollama, RAG y fuentes documentales, streaming y persistencia entre sesiones siguen pendientes.

### Siguiente paso propuesto
Elegir entre streaming en el chat (cambio pequeño) o empezar la ingesta documental con fuentes, que es el objetivo inicial del proyecto. La ingesta documental requiere un modelo avanzado de IA por el diseño de troceado, almacenamiento y citación.

## Actualización empresarial y documentos iniciales — 2026-09-13

Responsable: Codex, por petición expresa del usuario de corregir el contexto y elaborar documentos. Fuente: aclaración del usuario en esta conversación. Esta actualización es documental; no cambia el código ni las verificaciones técnicas históricas.

- Creado `CONTEXTO_NEGOCIO.md` como contexto empresarial duradero: aplicaciones a medida y mantenimiento para negocios, desarrollo web, automatización e internacionalización.
- Actualizados `CLAUDE.md`, `README.md` y `TRASPASO_CLAUDE.md` para reflejar ese objetivo. El mensaje de traspaso deja de presentar como pendientes la creación del chat y la publicación inicial en GitHub, ya documentadas.
- Creados tres borradores en `data/documentos/`: `01_presentacion_interemprex.md`, `02_catalogo_servicios_interemprex.md` y `03_proceso_trabajo_interemprex.md`.
- Cada documento identifica versión, fuente y condición de borrador. El objetivo empresarial está confirmado; el alcance detallado de servicios y el proceso de trabajo son propuestas para revisión, no compromisos comerciales aprobados.
- No se han inventado tarifas, plazos, clientes, mercados atendidos, garantías ni niveles de soporte. Internacionalización es un objetivo confirmado, con servicios concretos todavía por delimitar.
- Los documentos en `data/` quedan excluidos de Git por la regla existente. No se han incorporado al chat ni se ha implementado RAG. No se ha realizado commit ni publicación de esta actualización.
- Claude Code debe leer el nuevo contexto y este estado al retomar. Las copias subidas a Claude web no se sincronizan automáticamente y deben reemplazarse manualmente si se utilizan.

Siguiente paso: revisar los tres borradores con el usuario antes de tratarlos como fuentes empresariales aprobadas. Después diseñar la ingesta documental con fuentes, avisando de la conveniencia de usar un modelo avanzado de IA. Se mantiene el protocolo de un solo asistente editor a la vez.

## Revisión de los borradores de negocio — 13 de septiembre de 2026 — Claude Code (Opus 5) en F

Ejecutado en F (DESKTOP-T6C436J), carpeta original. Claude Code es el único editor de esta tarea. **No se ha tocado código, no se ha hecho commit y no se ha publicado nada.** Los cambios locales previos de Codex (`CLAUDE.md`, `README.md`, `TRASPASO_CLAUDE.md`, `ESTADO_PROYECTO.md` y `CONTEXTO_NEGOCIO.md` sin seguimiento) se han conservado intactos: las ediciones de esta sesión afectan solo a `data/documentos/` y a este archivo.

### Comprobaciones previas
- `data/` sigue excluido de Git por `.gitignore:8`, verificado con `git check-ignore -v` y con `git status`, que no muestra ningún archivo de `data/`.
- Árbol en `main`, sincronizado con `origin` en `e7bc39d`. No se ha añadido ningún commit en esta sesión.

### Hallazgo técnico relevante para la futura ingesta
Los tres documentos están en **UTF-8 correcto** en disco; las secuencias corruptas que aparecían en una copia pegada eran un problema de la copia, no del archivo.

Sin embargo, la codificación por defecto de Python en F es **cp1252**. Comprobado: abrir estos archivos sin `encoding="utf-8"` no degrada el texto, sino que **falla** con `UnicodeDecodeError: 'charmap' codec can't decode byte 0x81`. Cualquier ingesta documental deberá abrir los archivos con `encoding="utf-8"` explícito. Es un fallo que habría aparecido el primer día.

### Tamaño de los documentos frente al contexto actual
Medido con `estimar_tokens()` del propio proyecto, tras las correcciones:

| Documento | Caracteres | Tokens estimados |
|---|---|---|
| 01_presentacion_interemprex.md | 3257 | 1035 |
| 02_catalogo_servicios_interemprex.md | 4716 | 1499 |
| 03_proceso_trabajo_interemprex.md | 5020 | 1594 |
| **Suma** | **12993** | **4128** |

El presupuesto de entrada del chat es de 3456 tokens estimados y `num_ctx` es 4096. **Los tres documentos juntos no caben**; cualquiera por separado sí, y también caben dos de ellos. Esto condiciona el diseño de la primera prueba y, más adelante, obliga a elegir entre recuperar fragmentos (RAG) o ampliar `num_ctx`, lo que consumiría más VRAM.

### Revisión de contenido: qué se comprobó
1. **Coherencia con el objetivo confirmado.** Los tres reflejan la definición vigente de `CONTEXTO_NEGOCIO.md`. INT-PRES-001 §1 la reproduce casi literalmente; INT-SERV-001 organiza sus cinco secciones según los cinco ámbitos; INT-PROC-001 la cita en su cabecera. No se encontró ninguna contradicción con el contexto del proyecto.
2. **Ausencia de invenciones.** No aparecen tarifas, plazos, clientes, garantías, países ni prestaciones concretas de internacionalización. INT-SERV-001 §3 precisa que tienda online, marketing, SEO continuo y creación de contenidos **no quedan incluidos por el mero hecho de contratar desarrollo web**. Eso delimita el alcance de un encargo concreto; NO equivale a una decisión de excluir esas actividades del negocio, que sigue sin tomarse.
3. **Separación de hechos, propuestas y pendientes.** Correcta y explícita. Los documentos incluyen declaraciones expresas de ausencia («no existe **en este borrador** una garantía de soporte 24/7 ni un plazo de resolución aprobado», «no consta que INTEREMPREX ofrezca representación aduanera…»). Son declaraciones de que algo no está aprobado ni consta, NO negativas definitivas. Permiten que el asistente reconozca lo que falta en vez de inventarlo y, con el mismo cuidado, que no convierta esa ausencia en un «no» rotundo.

### Inconsistencias corregidas
Los tres documentos pasan a **versión 0.2** con una línea de revisión fechada. Correcciones aplicadas:

1. **Procedencia desigual.** INT-PRES-001 citaba `CONTEXTO_NEGOCIO.md` como fuente; INT-SERV-001 no lo hacía e INT-PROC-001 usaba un campo `Base:` distinto. Los tres tienen ahora la misma línea `Fuente principal:` apuntando a `CONTEXTO_NEGOCIO.md`. Para un asistente que debe citar, la procedencia uniforme es un requisito, no un detalle de estilo.
2. **Referencias cruzadas ausentes.** Solo INT-PRES-001 tenía sección de documentos relacionados. Se añadieron INT-SERV-001 §7 e INT-PROC-001 §10, y se amplió INT-PRES-001 §6 para señalar que `CONTEXTO_NEGOCIO.md` es la referencia vigente y que la presentación no la sustituye.
3. **Recorrido interno divergente.** INT-PROC-001 §8 describía «LeadFinder → evaluación → CRM → propuesta → cliente → operación», omitiendo la etapa *pipeline* que sí figura en `TRASPASO_CLAUDE.md`. Alineado a «LeadFinder → evaluación (scoring) → CRM → pipeline → propuesta → cliente → operación», citando el documento de origen.

Verificado tras editar: los tres siguen siendo UTF-8 válido, sin secuencias de doble codificación.

### Revisado y deliberadamente NO modificado
INT-SERV-001 alterna «Objetivo confirmado» (secciones 1 y 2) y «Ámbito confirmado» (secciones 3 a 5). Parecía una inconsistencia de etiquetado, pero responde a una distinción real que INT-PRES-001 §1 también hace: aplicaciones a medida y mantenimiento son el núcleo, mientras que web, automatización e internacionalización son ámbitos incluidos. Se deja como está.

### Aptitud como fuente del futuro asistente
Favorable, con reservas. A favor: identificador estable por documento (INT-PRES-001, INT-SERV-001, INT-PROC-001), versión y fecha, encabezados numerados y uniformes (`## N. Título`) que sirven de anclaje de cita, y declaraciones explícitas de ausencia que permiten responder «no consta». En contra: el título «Catálogo inicial de servicios» puede leerse como oferta comercial pese a su estado de borrador. Cambiar ese título **no obliga a cambiar el identificador**: el ID es independiente del título y del nombre de archivo, y conservarlo mantiene válidas las citas ya emitidas. Cada cita debe incluir ID, versión y sección, y el estado «borrador» debe viajar con ella.

### Pendientes
- Los tres documentos siguen siendo **borradores** y no deben usarse como política comercial hasta que se resuelvan las decisiones pendientes. Esas decisiones son comerciales y **no impiden las pruebas técnicas** sobre los documentos, que pueden ejecutarse mientras tanto.
- Ollama no estaba activo durante esta revisión; no se ejecutó ninguna inferencia. La prueba de consulta documental queda propuesta, no ejecutada.
- Sin cambios en el código, en la publicación ni en la configuración.

### Siguiente paso propuesto
Ejecutar la prueba base de consulta documental con citas (P0), descrita en la conversación: un solo documento en el contexto, ocho preguntas, verificación manual de que cada cita existe realmente. No es RAG y no requiere tocar el código del chat; el guion de prueba debe vivir fuera del repositorio. Solo después, y avisando de la conveniencia de usar un modelo avanzado de IA, diseñar la ingesta documental.

## Prueba P0 ejecutada — 13 de septiembre de 2026 — Claude Code (Opus 5) en F

Ejecutado en F (DESKTOP-T6C436J), carpeta original, con el Python de `.venv`. Claude Code, único editor. **Sin commit, sin push.** `data/` sigue excluido de Git, verificado tras la ejecución. No se modificó `chat_ollama.py` ni `probar_ollama.py`; el guion importa `estimar_tokens()` en modo lectura y vive fuera del repositorio, en `C:\Users\Fer\AppData\Local\Temp\claude\p0_interemprex\p0_prueba.py`. No se implementó RAG.

### Correcciones de interpretación previas
El usuario corrigió cuatro lecturas erróneas de la revisión anterior, y se aplicaron a este archivo y a las respuestas esperadas de la prueba:

1. Marketing, ecommerce y SEO **no quedan incluidos automáticamente** al contratar desarrollo web. Eso limita el alcance de un encargo; no es una decisión de excluirlos del negocio, que sigue sin tomarse.
2. Que no exista una garantía de soporte 24/7 aprobada **no equivale a negar** que pueda ofrecerse. Es ausencia de confirmación, no negativa.
3. Cambiar el título de un documento **no obliga a cambiar su identificador**. El ID es independiente del título y del nombre de archivo; conservarlo mantiene válidas las citas ya emitidas. Cada cita debe llevar ID, versión y sección.
4. Las decisiones comerciales pendientes **no impiden** las pruebas técnicas sobre los documentos.

### Condiciones de ejecución
- Se comprobó primero si Ollama respondía: no lo hacía. Se arrancó `ollama serve` en F y la API respondió en 2 s, versión 0.33.3. Ese proceso queda activo y no sobrevive a un reinicio.
- Archivos leídos con `encoding="utf-8"` explícito, como exige el hallazgo previo de que la codificación por defecto en F es cp1252.
- Modelo qwen3:8b, `num_ctx` 4096, `num_predict` 400, `temperature` 0.2, `think` desactivado.
- Cada pregunta se envió de forma independiente: instrucciones más un único documento completo, sin historial y sin arrastrar turnos anteriores.

### Presupuesto de contexto: estimado frente a real
Se midieron ambos. El estimador del proyecto dio entre 1314 y 1878 tokens; `prompt_eval_count`, que es el recuento real del tokenizador, dio entre 1065 y 1485. **El estimador sobreestimó un 24% de media**, coherente con el +35% medido antes en prosa. Sobra margen, que es el lado seguro del error. Ningún caso se acercó al límite de 4096.

### Resultado
Dos rondas de ocho preguntas, 16 respuestas. Las comprobaciones automáticas (estructura de la cita, fórmulas de ausencia, ausencia de cifras o países inventados) dieron **14 de 16 correctas**. La verificación manual contra el texto citado da un resultado **bastante peor**, y esa diferencia es el hallazgo principal de la prueba.

| # | Pregunta | Automático | Verificación manual | Motivo |
|---|---|---|---|---|
| 1 | ¿A qué se dedica INTEREMPREX? | OK | **Correcta** | §1 respalda la respuesta literalmente |
| 2 | ¿Entregables de una aplicación a medida? | OK | **Correcta** | §1 respalda y los llama «propuestos» |
| 3 | ¿Qué ocurre tras validación y entrega? | FALLA | **Fallo** | §7 respalda el contenido, pero lo presenta como procedimiento vigente y no como propuesta |
| 4 | ¿Cuánto cuesta una aplicación? | OK | Parcial | No inventa importe, pero responde «no consta» cuando §1 dice que presupuesto está *pendiente de acuerdo* |
| 5 | ¿Ofrece soporte 24/7? | OK | **Fallo** | §2 sí trata el asunto: dice que no hay garantía aprobada *en este borrador*. Responder «no consta» omite lo que el documento afirma |
| 6 | ¿En qué países trabaja? | OK | Parcial | No inventa países, pero §3 dice «pendientes de definir», no que no conste |
| 7 | ¿Propiedad del código fuente? | OK | Parcial | §1 lo marca como *pendiente de acuerdo*; «no consta» no es lo mismo |
| 8 | ¿Web incluye marketing, ecommerce y SEO? | OK | **Fallo** | §3 responde directamente a la pregunta. «No consta» es sencillamente falso |

Correctas 2, parciales 3, fallos 3. Las dos rondas fueron prácticamente idénticas: solo variaron una conjunción en P1 y un punto en P8. Con `temperature` 0.2 el comportamiento es estable, así que estos fallos son sistemáticos, no ruido de muestreo.

### Diagnóstico: el modelo colapsa cuatro situaciones distintas en una
El patrón es claro y afecta a cinco de las ocho preguntas. El asistente reduce a «No consta en el documento facilitado» cuatro casos que el documento distingue:

1. El dato no aparece.
2. El documento dice que está **pendiente de acuerdo** (P4, P7).
3. El documento dice que **no está aprobado en este borrador** (P5).
4. El documento **responde**, fijando un límite de alcance (P8).

Los casos 2, 3 y 4 son contenido presente en el documento, no ausencia. Responder «no consta» en ellos es una pérdida de información y, en P8, directamente incorrecto.

**Parte de la culpa es de las instrucciones, no del modelo.** La regla 2 del guion ofrecía una fórmula única y cómoda, «No consta en el documento facilitado», sin exigir distinguir entre ausencia real y contenido que declara algo pendiente. El modelo tomó el camino más barato. Esto se corrige en el diseño del prompt, y es precisamente lo que la prueba debía descubrir antes de construir el RAG encima.

### Por qué las comprobaciones automáticas no bastaron
P5 y P8 pasaron todos los filtros automáticos: citaban ID, versión y una sección existente, e incluían una fórmula de ausencia. Eran respuestas bien formadas y sustantivamente equivocadas. Ninguna comprobación de formato podía detectarlo: hizo falta abrir la sección citada y comparar. Esto confirma que la verificación manual contra el texto citado no es un extra, sino el núcleo de la prueba.

### Evidencia guardada
`data/pruebas/p0_2026-09-13_1044.md` (registro legible con pregunta, respuesta, tokens estimados y reales, secciones citadas y el texto real de cada sección citada para poder contrastarla) y `p0_2026-09-13_1044.json` (datos en bruto). Ambos dentro de `data/`, por tanto fuera de Git.

### Conclusión sobre el umbral para pasar a RAG
**No se alcanza.** El criterio era 8 de 8 con citas verificadas en dos rondas; el resultado verificado es 2 correctas, 3 parciales y 3 fallos. El formato de cita funciona bien —ID, versión y sección aparecieron siempre y ninguna sección citada era inexistente—, pero la interpretación de ausencia frente a contenido pendiente no es fiable todavía.

### Siguiente paso propuesto
Repetir P0 con instrucciones corregidas que obliguen a distinguir los cuatro casos, antes de tocar nada de recuperación. Es un cambio de prompt, barato, y si mejora se habrá aprendido algo aplicable directamente al RAG. Solo después diseñar la ingesta documental, fase para la que conviene un modelo avanzado de IA por el diseño de troceado, almacenamiento y formato de cita.

### Pendientes sin cambios
Los tres documentos siguen siendo borradores versión 0.2; las decisiones comerciales siguen abiertas y no bloquean estas pruebas. Arranque persistente de Ollama, RAG, streaming y persistencia entre sesiones siguen pendientes. No se ha publicado nada.

## Prueba P0 v2 ejecutada — 13 de septiembre de 2026 — Claude Code (Opus 5) en F

Ejecutado en F (DESKTOP-T6C436J), carpeta original, Python de `.venv`. Único editor. **Sin commit ni push.** `data/` excluido de Git, verificado. No se tocó `chat_ollama.py` ni `probar_ollama.py` ni se reinstaló nada. No se implementó RAG. Los documentos comerciales **no se modificaron** para facilitar el aprobado: siguen en la versión 0.2 revisada esta mañana. La prueba v1 y sus resultados se conservan íntegros.

### Corrección del diagnóstico anterior
El usuario señaló que las reglas 3 y 4 del prompt v1 **ya exigían** distinguir propuestas y condiciones pendientes. Es cierto, y eso invalida la explicación «el prompt no lo pedía» que se había dado. El diagnóstico pasó a tratarse como hipótesis falsable, reformulada así: el problema no era la ausencia de instrucción, sino que **una fórmula literal concreta compitió con reglas abstractas y ganó**. La regla 2 ofrecía una cadena exacta lista para copiar, aparecía antes que las reglas 3 y 4, y la regla 5 imponía un tope de 6 líneas.

Criterios de evaluación, preguntas nuevas e hipótesis se fijaron **antes** de ejecutar, en `data/pruebas/p0v2_criterios_preregistrados.md`.

### Qué cambió en la v2
Instrucciones reordenadas para exigir empezar por lo que la fuente sí dice; se eliminó la cadena literal única; se retiró el tope de brevedad; se añadió la prohibición de inventar una sección para respaldar una ausencia total. Parámetros idénticos a la v1 para que la comparación valga: qwen3:8b, num_ctx 4096, num_predict 400, temperature 0.2, think desactivado, dos rondas, cada pregunta independiente con un solo documento y sin historial. Ninguna respuesta se truncó. Las respuestas esperadas **no** se enviaron al modelo.

Se corrigió además el defecto del registro señalado por el usuario: la v1 recortaba las secciones citadas a 700 caracteres. La v2 guarda las **24 secciones citadas completas**, y además el prompt exacto, los parámetros y copias de los tres documentos tal como se enviaron.

### Resultado en significado — preguntas originales (1-8)

| # | Ronda 1 | Ronda 2 | Motivo |
|---|---|---|---|
| 1 | Correcta | Correcta | §2 respalda; añade que los ámbitos no acreditan catálogo disponible |
| 2 | Correcta | Correcta | Dice «entregables propuestos» |
| 3 | **Contradictoria** | **Contradictoria** | §7 respalda el contenido, pero lo presenta como fase vigente y no como *Propuesta* |
| 4 | Correcta | Correcta | Indica que no hay coste concreto **y** que debe definirse antes de una oferta vinculante |
| 5 | Correcta | Correcta | «No existe **en este borrador** una garantía de soporte 24/7». Conserva el estatus |
| 6 | Correcta | Correcta | «Pendientes de definir», no «no consta» |
| 7 | Correcta | Correcta | «Pendiente de acuerdo» |
| 8 | Correcta | Correcta | «No incluye **automáticamente**… por el mero hecho de contratar» |

Totales por ronda: 7 correctas y 1 contradictoria en cada una.

### Resultado en significado — preguntas nuevas (9-12)

| # | Tipo | Ronda 1 | Ronda 2 | Motivo |
|---|---|---|---|---|
| 9 | Reformulación de P5 | **Contradictoria** | **Contradictoria** | Afirma que «el mantenimiento incluye canales y horario de atención». §2 los lista como *pendientes de acuerdo*, no como incluidos |
| 10 | Reformulación de P8 | Correcta | Correcta | Conserva «no se incluye automáticamente» y cita el texto literal |
| 11 | Ausencia real | **Inventada** | **Inventada** | Acierta que no se menciona, pero atribuye la ausencia a «sección 1 a 6», que no la respalda |
| 12 | Ausencia real | **Inventada** | **Inventada** | Acierta que no se menciona, pero cita §1 como si respaldara la ausencia |

Totales por ronda: 1 correcta (P10), 1 contradictoria (P9) y 2 inventadas (P11 y P12).

**Corrección aplicada el mismo día.** En una primera lectura P11 y P12 se dieron por correctas porque su contenido acierta: el documento efectivamente no menciona plantilla ni año de fundación. Pero el criterio preregistrado califica de **Inventada** el hecho de «citar una sección que no respalda lo afirmado, incluido inventar una sección para justificar una ausencia total», y eso es exactamente lo que hacen. Se reclasifican. El criterio preregistrado prevalece sobre el juicio posterior; lo contrario vaciaría de sentido haberlo fijado antes.
### Totales globales
24 respuestas, valorando **el contenido**: 16 correctas, 4 contradictorias, 0 incompletas y 4 inventadas.

Este recuento NO es un aprobado de las respuestas en conjunto. Mide la fidelidad del contenido y deja fuera la calidad de la cita, que se evalúa aparte y fue mala: la versión faltó en 24 de 24. Una respuesta puede tener el contenido correcto y ser inservible como fuente citable. Lo que sí es cierto es que no se fabricó ningún dato de negocio: ni importes, ni países, ni años, ni plantillas, y ninguna sección citada era inexistente.

### Comparación con la v1, reevaluada con los mismos criterios
Para que la comparación sea honesta se reclasificó la v1 con la tabla preregistrada, más estricta que el juicio informal de entonces:

| | v1 (8 originales) | v2 (8 originales) |
|---|---|---|
| Correctas | 2 | 7 |
| Incompletas | 1 | 0 |
| Contradictorias | 5 | 1 |
| Cita con ID real | 16/16 | 19/24 |
| Cita con versión | **16/16** | **0/24** |
| Secciones inexistentes | 0 | 0 |

### Conclusión: la hipótesis queda respaldada, y de forma inesperada
El cambio de prompt corrigió cinco de las seis respuestas defectuosas en significado. Eso apoya la hipótesis. Pero lo decisivo es el **efecto espejo** en la cita de versión:

- En la v1 el ejemplo de formato contenía la cadena literal `v0.2`. El modelo la copió y la versión se citó correctamente en el 100% de los casos.
- En la v2 el ejemplo era el marcador abstracto `(ID vVERSIÓN, sección N)`. El modelo lo copió **también literalmente**: cinco respuestas escribieron «ID vVERSIÓN» tal cual, y la versión real desapareció del 100% de las respuestas.

El mecanismo es el mismo en los dos casos y explica ambos resultados. **Hipótesis apoyada por estos casos**: el modelo tiende a reproducir literalmente los ejemplos del prompt en lugar de instanciar patrones abstractos. En la v1 eso acertó por casualidad con la versión y falló con el matiz; en la v2 acertó con el matiz y arruinó la versión. Conviene no presentarlo como una limitación general demostrada del modelo: son dos observaciones sobre un prompt, un modelo y doce preguntas, no una caracterización de su comportamiento.

Consecuencia directa para el diseño del RAG: **los metadatos de la cita no deben pedirse al modelo**. El identificador, la versión y la sección se conocen en el momento de recuperar el fragmento y deben adjuntarse por código. Pedir al modelo que reproduzca datos que no puede verificar introduce un fallo evitable.

### Patrón que persiste
Dos fallos sobreviven al cambio de prompt, ambos estables en las dos rondas con temperature 0.2, es decir sistemáticos y no ruido de muestreo:

1. **P3: no conserva el carácter de propuesta** cuando la marca está en el cuerpo de la sección (`Propuesta: …`) y no en su título. En P2 y P8, donde el matiz aparece en el propio sintagma que se copia («entregables propuestos», «no quedan incluidos por el mero hecho»), sí se conserva.
2. **P9: convierte una lista de pendientes en una lista de inclusiones.** §2 enumera «Pendiente de acuerdo: periodo de cobertura, canales y horario de atención…» y el modelo responde que el mantenimiento «incluye canales y horario de atención». Es la misma frase leída al revés.

Ambos apuntan a lo mismo: el modelo conserva el matiz cuando viaja pegado a las palabras que copia, y lo pierde cuando depende de un encabezado o de un conector situado al principio de la frase. Es una limitación de lectura, no de instrucciones.

Nota de transparencia sobre dos decisiones límite: en P8 ronda 2 y en P10 el modelo añade que el SEO «queda pendiente de acuerdo». §3 no lo dice de ese asunto en concreto; lo dice de otra lista. Se clasificaron como Correctas por tratarse de una paráfrasis defendible dentro de la misma sección, pero una lectura estricta las contaría como Inventadas. Se deja constancia en lugar de ocultar el criterio.

### Evidencia guardada, toda en `data/pruebas/` y por tanto fuera de Git
- `p0v2_criterios_preregistrados.md`: hipótesis, criterios y preguntas nuevas, fijados antes de ejecutar.
- `p0v2_2026-09-13_1052.md`: registro legible con pregunta, respuesta, tokens estimados y reales, indicadores objetivos y **secciones citadas completas**.
- `p0v2_2026-09-13_1052.json`: datos en bruto.
- `p0v2_2026-09-13_1052_prompt_y_parametros.txt`: prompt de sistema exacto y parámetros.
- `p0v2_2026-09-13_1052_copias_documentos/`: copia de los tres documentos tal como se enviaron.
- Se conservan `p0_2026-09-13_1044.md` y `.json` de la v1.

### Siguiente experimento propuesto, sin encadenarlo
No se realiza ningún ajuste más de forma automática. La propuesta es **dejar de pedir la cita al modelo**: construir el encabezado de procedencia por código a partir de los metadatos del documento y pedir al modelo únicamente el contenido de la respuesta. Eso aísla lo que el modelo hace mal (reproducir metadatos) de lo que hace razonablemente bien (reflejar el estatus del contenido), y es la forma en que tendrá que funcionar el RAG de todos modos. Queda a decisión del usuario.

### Pendientes sin cambios
Documentos en borrador 0.2; decisiones comerciales abiertas, que no bloquean estas pruebas. Arranque persistente de Ollama, RAG, streaming y persistencia entre sesiones siguen pendientes. El `ollama serve` lanzado sigue activo y no sobrevive a un reinicio.

## Prueba P0 v3 ejecutada — procedencia añadida por código — 13 de septiembre de 2026 — Claude Code (Opus 5) en F

Ejecutado en F (DESKTOP-T6C436J), carpeta original, Python de `.venv`. Único editor. **Sin instalaciones, sin commit y sin push.** `data/` excluido de Git, verificado. No se tocó `chat_ollama.py`, `probar_ollama.py` ni los documentos comerciales, que siguen en la versión 0.2. No se implementó RAG. Se conservan íntegras las pruebas v1 y v2 con toda su evidencia.

Objetivo acotado, aprobado por el usuario: comprobar si se pueden eliminar los errores de identificador y versión sin empeorar el contenido. **Esta prueba no pretendía resolver los fallos de interpretación**, y en efecto no los resuelve del todo.

### Diferencia única frente a la v2
Las reglas 4 y 5 de cita se sustituyen por una regla 4 que prohíbe al modelo generar referencias de cualquier clase. Las reglas 1 a 3 de contenido, los tres documentos, las doce preguntas y todos los parámetros (qwen3:8b, num_ctx 4096, num_predict 400, temperature 0.2, think desactivado, dos rondas, cada pregunta independiente) se mantienen sin cambios, para que la comparación aísle una sola variable.

El ID, la versión y el estado se extraen por código de la cabecera del archivo y se muestran aparte, bajo el rótulo **«Documento proporcionado al modelo»**, seguido de una advertencia explícita de que **no es una cita verificada**: indica qué documento se entregó, no que una afirmación concreta esté respaldada. Como se entrega el documento completo, la procedencia corresponde al documento entero y **no se añaden números de sección**.

### (a) Exactitud de los metadatos añadidos por código

| Comprobación | Resultado |
|---|---|
| Registros contrastados contra la cabecera real del archivo | 24 |
| Discrepancias | **0** |
| Respuestas en las que el modelo generó alguna referencia pese a la prohibición | **0 de 24** |

Se verificó además la ruta de error exigida, con una autocomprobación sobre cadenas sintéticas, sin tocar los documentos reales: ante un documento sin ID, sin versión, con ID duplicado o vacío, el extractor **informa del error y no inventa nada**. Ejemplo de salida real: `campo 'id' ambiguo, 2 apariciones: ['INT-TEST-001', 'INT-TEST-002']`.

### (b) Fidelidad del contenido — preguntas originales (1-8)

| # | Ronda 1 | Ronda 2 | Observación |
|---|---|---|---|
| 1 | Correcta | Correcta | Conserva la advertencia de que los ámbitos no acreditan catálogo disponible |
| 2 | Correcta | Correcta | «Entregables propuestos»; añade que están pendientes de concretar por proyecto |
| 3 | **Contradictoria** | **Contradictoria** | Persiste: presenta §7 como fase vigente, no como *Propuesta* |
| 4 | Correcta | Correcta | No hay coste concreto y debe definirse antes de una oferta vinculante |
| 5 | Correcta | Correcta | «No existe en este borrador una garantía de soporte 24/7» |
| 6 | Correcta | Correcta | «Pendientes de definir» |
| 7 | Correcta | Correcta | «Pendiente de acuerdo» |
| 8 | Correcta | Correcta | «Por el mero hecho de contratar»; se mantiene la atribución límite de «pendiente de acuerdo» |

Por ronda: 7 correctas, 1 contradictoria.

### (b) Fidelidad del contenido — preguntas nuevas (9-12)

| # | Ronda 1 | Ronda 2 | Observación |
|---|---|---|---|
| 9 | **Correcta** | **Correcta** | **Corregido**: ahora dice que periodo, canales y horario están *pendientes de acuerdo*. Desaparece el error de la v2, que los daba por incluidos |
| 10 | Correcta | Correcta | La ronda 2 mejora: «funcionalidad adicional que requiere definir y acordar», sin atribuir un estatus que la fuente no da |
| 11 | **Correcta** | **Correcta** | **Corregido**: dice que no se menciona, sin atribuir la ausencia a ninguna sección |
| 12 | **Correcta** | **Correcta** | **Corregido**, igual que P11 |

Por ronda: 4 correctas.

### Totales globales de la v3
24 respuestas: **22 correctas y 2 contradictorias** (P3 en ambas rondas). Cero incompletas y cero inventadas.

### Comparación de las tres versiones, con los mismos criterios

| | v1 | v2 | v3 |
|---|---|---|---|
| Originales, por ronda: correctas | 2 | 7 | 7 |
| Originales, por ronda: contradictorias | 5 | 1 | 1 |
| Originales, por ronda: incompletas | 1 | 0 | 0 |
| Nuevas, por ronda: correctas | — | 1 | **4** |
| Nuevas, por ronda: contradictorias | — | 1 | 0 |
| Nuevas, por ronda: inventadas | — | 2 | **0** |
| Versión citada correctamente | 16/16 (por el modelo) | **0/24** | **24/24 (por código)** |
| Identificador correcto | 16/16 (por el modelo) | 19/24 | **24/24 (por código)** |

### Qué queda resuelto y qué no
**Resuelto:** los errores de identificador y versión desaparecen por completo, y no a base de insistir al modelo, sino retirándole la tarea. Tampoco reaparecieron por su cuenta: ninguna de las 24 respuestas generó referencias. Y el contenido no empeoró, que era la condición del experimento: se mantuvo en las originales y mejoró en las nuevas, donde P9, P11 y P12 pasan a correctas.

**No resuelto:** P3 falla igual que en v1 y en v2, en las dos rondas y con temperature 0.2, es decir de forma estable. El modelo sigue presentando como procedimiento vigente lo que §7 marca con el prefijo `Propuesta:`. La procedencia por código **no corrige la interpretación**, tal como el usuario advirtió al aprobar la prueba.

Hay una mitigación parcial que conviene no confundir con una solución: como el bloque de procedencia incluye el campo `Estado`, la presentación final de P3 sí muestra «propuesta de procedimiento pendiente de aprobación; no es una metodología contractual ya implantada». El lector avisado lo verá. Pero el cuerpo de la respuesta sigue afirmando lo contrario, y quien lo lea por encima se quedará con el cuerpo.

### Limitaciones de esta prueba
- La procedencia es **de documento, no de afirmación**. Dice qué documento se entregó; no acredita que una frase concreta esté respaldada. Por eso se rotula «Documento proporcionado al modelo» y no «cita verificada». En cuanto haya recuperación de fragmentos, hará falta decidir cómo se acredita cada afirmación por separado, que es un problema distinto y más difícil.
- Se sigue entregando **el documento correcto ya elegido**. No hay recuperación, que es la parte que más falla en un RAG real.
- Doce preguntas, tres documentos pequeños, un solo modelo, temperature 0.2. No autoriza conclusiones generales sobre el comportamiento del modelo.
- Dos decisiones límite se mantienen declaradas: en P8 y en P10 ronda 1 el modelo atribuye al SEO el estatus «pendiente de acuerdo», que §3 da a otra lista. Se cuentan como correctas por ser paráfrasis defendible; una lectura estricta las contaría como inventadas.
- El estimador de tokens volvió a sobreestimar en torno a un 24% (1471-2035 estimados frente a 1183-1603 reales), coherente con las medidas anteriores.

### Evidencia guardada, toda en `data/pruebas/` y fuera de Git
`p0v3_<marca>.md` con, por pregunta, los metadatos extraídos, los tokens estimados y reales, los rastros de referencia, la **respuesta original del modelo sin retocar** y la **presentación final** entregada; `p0v3_<marca>.json` con los datos en bruto; `p0v3_<marca>_prompt_y_parametros.txt` con el prompt exacto y los parámetros; y `p0v3_<marca>_copias_documentos/` con copia de los tres documentos tal como se enviaron.

### Siguiente paso más pequeño propuesto, sin encadenarlo
Aislar si el fallo de P3 es **posicional**. La observación es que el matiz se conserva cuando viaja pegado a las palabras que el modelo copia («entregables propuestos», «por el mero hecho de contratar») y se pierde cuando vive en un prefijo al comienzo del párrafo (`Propuesta:`). El experimento mínimo sería preguntar por varias secciones de INT-PROC-001 que usan ese mismo prefijo, sin cambiar prompt, parámetros ni documentos, y contar en cuántas se conserva el carácter de propuesta. Si falla en todas, el problema es el prefijo y se resuelve en la ingesta, marcando el estatus en cada fragmento; si falla solo en algunas, la causa es otra. Queda a decisión del usuario.

## Primera versión utilizable de consulta documental — 13 de septiembre de 2026 — Claude Code (Opus 5) en F

Ejecutado en F (DESKTOP-T6C436J), carpeta original. Único editor. **Sin instalaciones, sin commit y sin push.** `data/` excluido de Git, verificado después de ejecutar. No se tocaron `chat_ollama.py`, `probar_ollama.py` ni los documentos comerciales, que siguen en versión 0.2. Se conservan las pruebas P0 v1, v2 y v3. Los cambios locales previos de Codex siguen intactos.

### Qué se ha construido
`consultar_documentos.py`, en la raíz del proyecto. Se escribe una pregunta y devuelve las secciones más parecidas de los tres documentos, **sin necesidad de elegir antes el documento correcto**. Solo biblioteca estándar: no hay base de datos, ni índice persistente, ni modelo de embeddings, ni instalación nueva.

**Deliberadamente NO consulta a ningún modelo de lenguaje.** La prueba P0 dejó abierto el fallo P3: el modelo pierde el carácter de propuesta de los procedimientos marcados con el prefijo `Propuesta:`. Mientras eso siga así, esta versión entrega el texto sin intermediario. Es la base verificable sobre la que integrar después la respuesta del modelo.

### Cómo busca
- Cada una de las 23 secciones de los tres documentos es un fragmento independiente, con su ID, versión, estado, número y título de sección, y su texto literal.
- Normaliza mayúsculas y acentos, descarta palabras vacías y recorta plurales de forma muy básica.
- Puntúa al estilo BM25: un término que aparece en muchas secciones pesa poco, repetir un término suma cada vez menos, y las secciones largas no ganan por tamaño. Coincidir en el **título** de la sección pesa el triple.
- Exige una coincidencia mínima: o bien un término poco común, o bien dos términos distintos. Así una sola palabra omnipresente no arrastra resultados.

### Cómo presenta
Antes del texto de cada sección se muestran, por este orden: identificador, versión, número y título de sección, archivo, **estado del documento** y **avisos sobre la sección**, extraídos por código de marcas que el propio texto usa (`Propuesta:`, `Alcance propuesto`, `Entregables propuestos`, `Pendiente de acuerdo`, `Pendiente de definir`, `Resultado esperado`, `Objetivo confirmado`, `Ámbito confirmado`). Después, el texto **literal**, sin resumir ni reformular.

Esto ataca P3 por otra vía: un procedimiento propuesto aparece rotulado como «PROCEDIMIENTO PROPUESTO, pendiente de aprobación» **antes** de que se lea el texto, y el texto conserva su prefijo `Propuesta:`. No lo resuelve en la respuesta de un modelo, pero impide que la consulta directa lo presente como acordado.

### Dos fallos encontrados y corregidos durante la construcción
1. **Codificación de la entrada.** La consola interactiva funciona, pero al redirigir la entrada Python la lee como cp1252 y las preguntas llegaban corrompidas: «internacionalización» se convertía en «internacionalizacia» y no encontraba nada. Se reconfiguran `stdin` y `stdout` a UTF-8. Detectado porque dos preguntas devolvían cero resultados sin motivo aparente.
2. **El nombre de la empresa contaminaba el ranking.** Con «interemprex» como término buscable, la pregunta «¿qué servicios de automatización ofrece INTEREMPREX?» colocaba primera una sección genérica (1,16 puntos) por delante de la sección «Automatización» (0,90), porque coincidía en dos términos en vez de uno. El nombre aparece en los tres documentos y no puede distinguir entre ellos, así que pasa a la lista de palabras vacías. Medido antes y después, no supuesto.

### Verificación ejecutada
Siete preguntas sobre actividad, servicios, mantenimiento, proceso y una sin respuesta posible. **La búsqueda eligió sola**: no se le pasó el documento esperado ni hay respuestas codificadas para las preguntas de prueba.

| Pregunta | Primer resultado | Valoración |
|---|---|---|
| ¿A qué se dedica INTEREMPREX? | sin resultados, muestra el índice de secciones | Límite real: «dedica» no aparece en los documentos |
| ¿Cuál es el objetivo de la empresa? | INT-PRES-001 §3 «A quién se dirige» | Parcial: §1 y §2, más pertinentes, salen 2.º y 3.º |
| ¿Qué servicios de automatización ofrece? | INT-SERV-001 §4 «Automatización» | Correcto |
| ¿Qué incluye el mantenimiento de una aplicación? | INT-PRES-001 §1 «Qué es INTEREMPREX» | Parcial: §2 «Mantenimiento de las soluciones» sale 2.º |
| ¿Cómo es el proceso de trabajo desde el primer contacto? | INT-PROC-001 §1 «Primer contacto y necesidad» | Correcto |
| ¿Qué entregables tiene el desarrollo web? | INT-SERV-001 §3 «Desarrollo web» | Correcto |
| ¿En qué año se fundó la empresa? | INT-PRES-001 §3, con aviso de términos ausentes | Correcto como límite: avisa de que «ano» y «fundo» no están en ningún documento |

Comprobación automática de integridad, contrastando cada fragmento con el archivo de origen: **23 secciones, 0 fallos**. El texto mostrado existe literalmente en el archivo, los metadatos coinciden con la cabecera real y no se pierde ninguna sección (6, 7 y 10 respectivamente).

### Limitaciones de la búsqueda, comprobadas
- **Compara palabras, no significados.** Si la pregunta usa un sinónimo que el documento no emplea, no encuentra nada. «¿A qué se dedica?» es el ejemplo: el documento nunca usa «dedicarse». Por eso, cuando no hay resultados, se muestra el índice completo de secciones para que se pueda ir directo.
- **Una sección corta y general puede adelantar a la específica.** Ocurre con mantenimiento y con objetivo. Se mitiga mostrando tres resultados, no uno. No se ha ajustado la fórmula para forzar los resultados de estas preguntas concretas: hacerlo sería adaptar el buscador al examen.
- **Un resultado no es una respuesta.** La búsqueda devuelve secciones que contienen las palabras, y no sabe si responden. Por eso avisa de qué términos de la pregunta no existen en ningún documento, y de cuándo la coincidencia es débil.
- **No encontrado no es una negativa comercial.** El mensaje lo dice expresamente: que algo no esté escrito en tres borradores iniciales no significa que INTEREMPREX no lo ofrezca.
- El recorte de plurales es rudimentario y puede fallar con formas irregulares. No hay lematizador en la biblioteca estándar.
- Solo tres documentos y 23 secciones. Con muchos más documentos, este método por palabras se quedará corto y habrá que revisarlo.

### Evidencia guardada, toda en `data/` y fuera de Git
`data/pruebas/verificacion_consultar_documentos_2026-09-13.txt` con la sesión completa de verificación. Además, el propio programa guarda un registro de cada sesión en `data/consultas/`, con la pregunta, los términos buscados y los fragmentos devueltos.

### Siguiente paso propuesto
Integrar la respuesta del modelo **sobre** estos fragmentos, no en lugar de ellos: que el buscador elija las secciones y el modelo redacte encima, manteniendo visible el texto literal y los avisos de estado. El fallo P3 sigue abierto y es justo lo que habrá que vigilar en esa integración. Queda a decisión del usuario.

## Primera versión del asistente documental — 13 de septiembre de 2026 — Claude Code (Opus 5) en F

Ejecutado en F (DESKTOP-T6C436J), carpeta original. Único editor. **Sin instalaciones, sin commit y sin push.** `data/` excluido de Git. No se tocaron `chat_ollama.py`, `probar_ollama.py` ni los documentos comerciales, que siguen en versión 0.2. Se conservan todas las pruebas anteriores.

### Qué se ha construido
`asistente_documental.py`, en la raíz. Une el buscador ya entregado con qwen3:8b en Ollama. Se escribe una pregunta y devuelve, por este orden: una respuesta breve apoyada solo en los fragmentos, los **Fragmentos consultados** con su procedencia añadida por código, y el texto literal de cada uno para contrastar.

Reutiliza `consultar_documentos.py` tal cual, e importa `estimar_tokens()` de `chat_ollama.py` en modo lectura para medir con el mismo criterio de siempre. Cada pregunta es independiente: no hay historial.

### Correcciones previas exigidas
- **Mensaje «sin resultados» corregido.** Ya no afirma que las palabras falten en los documentos. Ahora dice que *esta búsqueda* no las ha casado, y explica que antes de buscar se descartan palabras comunes, se recortan plurales de forma rudimentaria y se exige una coincidencia mínima, de modo que un término escrito puede quedar fuera. Sugiere abrir los archivos para salir de dudas. Igual se corrigió el aviso de términos no casados.
- **La puntuación ya no se presenta como garantía.** Tanto el buscador como el asistente indican que mide parecido de palabras y que una puntuación alta puede acompañar a un fragmento que no sirve.

### Dos fallos propios detectados y corregidos durante la construcción
1. **Repetí el error del atractor literal.** La primera versión de las instrucciones daba al modelo la frase exacta «Los fragmentos consultados no responden a esta pregunta» para los casos sin respuesta. El modelo la usó en la primera prueba real, sobre automatización, **cuando el fragmento sí respondía**. Es exactamente el mecanismo identificado en P0 v1: una cadena literal lista para copiar compite con las reglas abstractas y gana. Corregido: la regla 1 pasa a ser afirmativa («si algún fragmento trata el asunto, respóndelo, no te niegues porque falte un dato concreto») y la negativa queda condicionada y sin frase modelo.
2. **La salvaguarda de P3 era demasiado tosca.** Se disparaba si *cualquier* fragmento enviado era un procedimiento propuesto, aunque la respuesta no lo usara; llegó a retener una simple negativa. Corregido: ahora compara el vocabulario distintivo del fragmento propuesto con el de la respuesta y solo actúa si comparten al menos cuatro términos poco comunes, es decir, si la respuesta realmente se apoya en él.

### Cómo se cumplen las condiciones
- **Presupuesto de contexto**: 4096 − 400 reservados para la respuesta − 128 de margen = 3568 tokens estimados, contando instrucciones, pregunta y fragmentos. Si una sección no cabe **entera se descarta completa** y se informa de ello; nunca se corta, porque partirla podría dejar fuera la condición que matiza el resto.
- **Procedencia por código**: identificador, versión, estado y sección se leen de la cabecera del archivo. El modelo tiene prohibido escribir referencias. El bloque se rotula **«Fragmentos consultados»**, con la advertencia expresa de que son los fragmentos entregados y no afirmaciones verificadas.
- **Estado por delante del texto**: cada fragmento llega al modelo, y se muestra al usuario, con el estado del documento y los avisos de la sección antes del texto.
- **Ollama apagado**: mensaje claro, comando exacto para arrancarlo, y **se siguen mostrando los fragmentos encontrados**, que no dependen del modelo. El bucle continúa.
- **Sin fragmentos**: no se llama al modelo y se explica el límite de la búsqueda.

### Resultados reales de la verificación
Seis preguntas, con la búsqueda eligiendo sola los fragmentos:

| Pregunta | Resultado |
|---|---|
| ¿Qué servicios de automatización ofrece? | Correcta. Conserva «alcance propuesto», «entregables propuestos» y «pendientes de acuerdo» |
| ¿Qué incluye el mantenimiento de las soluciones? | Correcta. Conserva lo pendiente de acuerdo y que no hay garantía de 24/7 aprobada **en este borrador** |
| ¿Qué ocurre después de la validación y entrega? | **Redacción retenida** por la salvaguarda P3 |
| ¿Cómo es el proceso de trabajo desde el primer contacto? | Correcta. La respuesta sí dice «propuesta de procedimiento pendiente de aprobación» |
| ¿En qué año se fundó la empresa? | Correcta. «No figura en estos documentos», sin inventar |
| ¿Ofrecéis contabilidad y nóminas? | Correcta. «No consta en estos documentos», sin convertirlo en negativa comercial |

Contexto medido en las seis: entre 514 y 958 tokens reales de entrada, frente a 617-1223 estimados. El estimador vuelve a sobreestimar en torno al 24%, coherente con todas las medidas anteriores. Ninguna consulta se acercó al límite de 3568.

### Estado del fallo P3: sigue abierto
La pregunta exacta que fallaba en P0, «¿Qué ocurre después de la validación y entrega?», **se repitió tres veces y falló las tres**. La respuesta describía §6 y §3 como lo que ocurre, sin indicar que son procedimientos propuestos. La salvaguarda la retuvo las tres veces y se comprobó a mano que no era un falso positivo.

En cambio, «¿Cómo es el proceso de trabajo desde el primer contacto?» sí conservó el carácter de propuesta. Dos observaciones no autorizan a concluir por qué una funciona y otra no; lo único demostrado es que **el fallo no está resuelto y que la comprobación por código lo detecta**.

Cuando la salvaguarda actúa, se muestra el texto literal con su marca «Propuesta:» intacta y se dice expresamente que la redacción se ha retenido y por qué. La respuesta original del modelo queda registrada en el archivo de la sesión, para poder revisarla.

### Limitaciones
- **La salvaguarda es un umbral, no una garantía.** Cuatro términos distintivos compartidos es un criterio ajustado a mano sobre estos documentos. Puede retener una respuesta correcta o dejar pasar una incorrecta que use pocas palabras del fragmento.
- **Basta con que la respuesta contenga la palabra «propuesta» para que pase el filtro.** No se comprueba que el matiz esté bien aplicado, solo que aparece.
- **La búsqueda manda.** Si elige mal los fragmentos, la respuesta será mala por muy bien que redacte el modelo. Sigue siendo coincidencia de palabras, sin significado.
- **Solo se envían hasta tres secciones.** Una pregunta cuya respuesta esté repartida entre más documentos quedará incompleta sin avisar.
- **Sin historial**: cada pregunta parte de cero, no se pueden encadenar repreguntas.
- **Seis preguntas, tres documentos, un modelo.** No autoriza conclusiones generales sobre fiabilidad.

### Evidencia guardada, toda en `data/` y fuera de Git
`data/pruebas/verificacion_asistente_documental_2026-09-13.txt` con la sesión completa de verificación. El programa guarda además cada sesión en `data/asistente/`, con la pregunta, los fragmentos entregados, los tokens estimados y reales, **la respuesta original del modelo sin retocar**, si fue retenida y por qué, y los fragmentos consultados.

### Siguiente paso, no iniciado
Queda pendiente decidir qué hacer con P3: o se investiga por qué unas preguntas conservan el matiz y otras no, o se acepta la salvaguarda como solución de compromiso y se pasa a otra cosa. También siguen abiertos el historial entre preguntas, el arranque persistente de Ollama y las decisiones comerciales sobre los borradores.

## Cierre de la primera versión del asistente para uso interno — 13 de septiembre de 2026 — Claude Code (Opus 5) en F

Ejecutado en F (DESKTOP-T6C436J), carpeta original. Único editor. **Sin instalaciones, sin commit y sin push.** `data/` fuera de Git. No se tocaron los documentos comerciales, `chat_ollama.py` ni `probar_ollama.py`. Se conservan todos los cambios y pruebas anteriores. No se abrió ninguna investigación nueva sobre P3.

### Cambio 1: la decisión sobre procedimientos propuestos pasa a ser previa a la generación
Se retira la salvaguarda anterior, que revisaba la respuesta ya escrita y la retenía si compartía al menos cuatro términos distintivos con un fragmento propuesto. En su lugar, la decisión se toma **antes** de llamar al modelo: si alguno de los fragmentos seleccionados está marcado como procedimiento pendiente de aprobación, no se consulta a Ollama y se entra en **modo literal**, mostrando el texto original con su estado.

Es más simple y más seguro: no hay redacción que revisar porque no se genera ninguna. Desaparecen el umbral ajustado a mano y el riesgo de que una respuesta problemática pasara el filtro por contener la palabra «propuesta».

### Cambio 2: se explica el motivo, y la regla se documenta como conservadora
El modo literal dice al usuario, en dos líneas, que no se ha redactado respuesta porque entre las secciones encontradas hay un procedimiento pendiente de aprobación, y que se entrega el texto tal cual para no presentarlo como la forma de trabajar vigente. Se nombra la sección concreta.

Queda escrito, en el propio código y aquí, que **la regla es deliberadamente prudente**: se activa aunque solo una de las secciones encontradas sea una propuesta y aunque esa sección sea poco pertinente para la pregunta.

**Cuánto cuesta esa prudencia, medido**: 7 de las 23 secciones están marcadas como procedimiento propuesto, y son todas las de INT-PROC-001 §1 a §7. Sobre una batería de 10 preguntas, **el modo literal se activó en 7**. Entre ellas, preguntas cuyo asunto principal no era el proceso de trabajo: «¿Qué entregables tiene el desarrollo web?» entra en modo literal porque la búsqueda arrastra INT-PROC-001 §2, y «¿Ofrece soporte 24/7?» y «¿Qué tarifas hay?» también. Es el comportamiento buscado, pero conviene saber que hoy la mayoría de consultas no se redactan.

### Cambio 3: las afirmaciones de ausencia se limitan a los fragmentos consultados
La instrucción 3 prohíbe ahora decir que algo falta en los documentos o que no está en ninguna parte, porque al modelo solo se le entregan algunas secciones sueltas y no puede saber qué dicen las demás. Comprobado en ejecución: a «¿En qué año se fundó la empresa?» respondió «No se menciona el año de fundación de la empresa **en los fragmentos proporcionados**».

Matiz honesto: no siempre acota con esa claridad. A «¿Cuántos empleados tiene la empresa?» respondió «No se especifica el número de empleados que tiene la empresa», sin decir respecto a qué. No afirma que falte en los documentos, así que no incumple la regla, pero tampoco la aplica de forma explícita. El comportamiento es correcto pero no uniforme.

### Cambio 4: en la prueba integrada de P3 no se recuperó §7
Dato comprobado sobre cinco ejecuciones registradas: para la pregunta «¿Qué ocurre después de la validación y entrega?», la búsqueda entregó siempre **INT-PROC-001 §6, INT-PROC-001 §3 e INT-SERV-001 §1**. La sección §7 «Mantenimiento y evolución» **nunca llegó al modelo**.

Esto obliga a separar dos cosas que se estaban mezclando:

- **El fallo P3 observado en P0** es de redacción: con §7 delante, el modelo la presentaba como procedimiento vigente. Se midió entregando el documento entero.
- **Lo observado en la versión integrada** es distinto: el modelo redactó §6 y §3 como vigentes, que es un fallo de la misma familia, pero **la pregunta que P0 examinaba nunca se puso a prueba**, porque su sección no se recuperó. Es un límite de la búsqueda, no del redactado.

Por indicación expresa del usuario **no se modifica el buscador** para que recupere §7 en esa pregunta concreta: adaptarlo a un caso conocido sería ajustar la herramienta al examen. Queda anotado como límite abierto.

### Comprobaciones ejecutadas
| Escenario | Resultado real |
|---|---|
| Consulta que usa el modelo | «¿A quién se dirige la empresa?» → respuesta correcta, conserva «pendientes de definir». «¿Qué condiciones comunes quedan pendientes?» → correcta |
| Consulta que activa el modo literal | «¿Qué ocurre después de la validación y entrega?» → no se llama al modelo; se muestran §6 y §3 literales con su estado y el motivo |
| Consulta sin información suficiente | «¿Cuántos empleados tiene la empresa?» → «No se especifica el número de empleados», sin inventar y sin negativa comercial |
| Ollama apagado | Mensaje claro, comando exacto para arrancarlo y **los fragmentos se siguen mostrando**. El bucle continúa |

Se corrigió además que `stderr` no estaba reconfigurado a UTF-8 y los acentos se corrompían al redirigir la salida.

### Limitaciones de esta versión, que se cierra para uso interno
- **Hoy la mayoría de las consultas no se redactan**: 7 de cada 10 en la batería de prueba entran en modo literal. Es seguro, pero el asistente se comporta a menudo como un buscador con explicación.
- El modo literal depende de una marca textual: que la sección empiece por `Propuesta:`. Si un documento futuro expresa lo mismo de otra forma, la regla no se activará.
- Las afirmaciones de ausencia se acotan casi siempre, pero no de manera uniforme.
- Sigue sin historial: cada pregunta parte de cero.
- La búsqueda manda: si elige mal, la respuesta será mala. Solo se envían hasta tres secciones.
- Diez preguntas, tres documentos, un modelo. No autoriza conclusiones generales de fiabilidad.

### Evidencia
`data/pruebas/verificacion_asistente_v2_2026-09-13.txt` con los cuatro escenarios, incluido el de Ollama apagado. Las sesiones siguen registrándose en `data/asistente/`, ahora anotando también cuándo se entró en modo literal y por qué.

### Siguiente fase, acordada y no iniciada
Simplificar el arranque diario y preparar el respaldo de esta versión. No se ha empezado.

## Arranque diario en un comando y copia de seguridad local — 13 de septiembre de 2026 — Claude Code (Opus 5) en F

Ejecutado en F (DESKTOP-T6C436J), carpeta original. Único editor. **Sin instalaciones, sin commit y sin push.** No se tocaron los documentos comerciales, `chat_ollama.py` ni `probar_ollama.py`. No se amplió el buscador ni se investigó P3. Se conservan todos los cambios y evidencias anteriores.

### 1. `iniciar_asistente.ps1`
Arranque en un solo comando desde la terminal PowerShell de F, incluida la remota de VS Code. Qué hace, por orden: localiza el proyecto desde su propia ubicación con `$PSScriptRoot`, comprueba que existen el Python de `.venv` y `asistente_documental.py`, consulta la API en `127.0.0.1:11434`, **reutiliza la instancia si ya responde**, y si no la localiza en `%LOCALAPPDATA%\Programs\Ollama`, en `%ProgramFiles%\Ollama` o en el PATH y la arranca en segundo plano con ventana oculta, redirigiendo salida y errores a `logs/`. Espera hasta 30 segundos y, si no arranca, explica qué mirar: el registro de errores, si el puerto 11434 está ocupado, cómo lanzarlo a mano y que existe `consultar_documentos.py` para trabajar sin modelo. Al salir del asistente **deja Ollama activo** para la siguiente consulta.

No instala nada, no crea servicios ni tareas de inicio y **no cambia la política de PowerShell**. No hace falta: la política del usuario es `RemoteSigned`, que permite ejecutar un `.ps1` local. El script se escribió **solo con caracteres ASCII** a propósito: Windows PowerShell 5.1 interpreta como ANSI los archivos sin BOM, y los acentos saldrían corruptos.

**Comprobado en ejecución, los dos caminos:**

| Situación | Resultado real |
|---|---|
| Ollama ya activo | «Ollama ya estaba activo (version 0.33.3). Se reutiliza.» No se lanzó una segunda instancia. El asistente respondió correctamente |
| Ollama detenido | Localizó `C:\Users\Fer\AppData\Local\Programs\Ollama\ollama.exe`, lo arrancó oculto, la API respondió y abrió el asistente. Se crearon `logs\ollama_2026-09-13_133925.log` y `.err.log` |
| Al salir | Proceso activo (PID 46140) y API respondiendo. Confirmado tras cerrar el asistente |

### 2. Copia de seguridad: `crear_copia_seguridad.ps1`
Genera un ZIP fechado en `C:\Users\Fer\Documents\Copias-INTEREMPREX`, **fuera del proyecto**, para que un borrado dentro de la carpeta de trabajo no se lleve también la copia.

Se incluye por **lista explícita**, no por exclusión. Es una decisión deliberada: si mañana aparece un archivo con credenciales o con conversaciones, no puede colarse por descuido, porque solo entra lo que está nombrado. La lista cubre código (6 programas más los dos scripts y `.gitignore`), documentación e instrucciones (7 archivos) y los tres documentos de negocio de `data/documentos/`, conservando la estructura de carpetas. El ZIP lleva dentro un `INVENTARIO.txt` con origen, equipo, fecha, tamaño de cada archivo, lista de lo excluido con su motivo, alcance de la copia e instrucciones de restauración.

Quedan fuera `.venv`, los modelos de Ollama, `__pycache__`, `logs/`, y los registros de `data/asistente/`, `data/consultas/` y `data/pruebas/`.

**Copia creada y verificada de forma independiente**, no solo con la comprobación del propio script: `testzip()` devolvió íntegro, 19 entradas (18 archivos más el inventario), 63,8 KB, estructura `data/documentos/` conservada y **ningún material excluido colado**.

**Alcance, dicho claramente**: esta copia está en el mismo disco que el proyecto. Protege frente a cambios o borrados accidentales, **no frente a una avería del equipo F**. Para eso haría falta otro soporte o un destino remoto, que no se ha configurado.

### 3. `GUIA_CONTINUIDAD.md` actualizada
La secuencia diaria pasa a seis pasos, de los que solo el último es un comando: encender F y comprobar Tailscale, abrir VS Code en el Mac, conectar por SSH a `ordenador-f`, abrir la carpeta original, abrir una terminal PowerShell remota y ejecutar `.\iniciar_asistente.ps1`. Se añadieron el atajo para consultar sin modelo y el de la copia de seguridad.

Se actualizó también la sección «Qué contiene el código», que seguía describiendo solo dos programas y omitía el asistente, el buscador y los dos scripts nuevos.

**El acceso desde el ordenador D no se presenta como verificado**: la guía dice expresamente que no está probado, igual que el acceso desde fuera de casa.

### Cambios todavía SIN publicar en GitHub
El último commit publicado sigue siendo `e7bc39d`. En el árbol de trabajo hay, sin confirmar:

| Estado | Archivo |
|---|---|
| Modificado | `CLAUDE.md`, `README.md`, `TRASPASO_CLAUDE.md` (contexto empresarial, por Codex) |
| Modificado | `ESTADO_PROYECTO.md`, `GUIA_CONTINUIDAD.md` |
| Nuevo | `CONTEXTO_NEGOCIO.md` (2,1 KB) |
| Nuevo | `consultar_documentos.py` (16,7 KB) |
| Nuevo | `asistente_documental.py` (15,4 KB) |
| Nuevo | `iniciar_asistente.ps1` (5,2 KB) |
| Nuevo | `crear_copia_seguridad.ps1` (6,3 KB) |

Es decir, **todo el trabajo de consulta documental y de arranque está sin respaldo en GitHub**. Hoy la única protección es el ZIP local, que está en el mismo disco. Publicar sigue siendo una decisión del usuario; no se ha hecho commit ni push.

`data/` continúa excluido de Git por diseño: los documentos de negocio, los registros de conversaciones y las evidencias de prueba no se publican.

### Limitaciones de esta fase
- El arranque hay que lanzarlo a mano: **no hay arranque desatendido tras reiniciar Windows**, ni servicio ni tarea programada, porque se pidió no configurarlos todavía.
- `iniciar_asistente.ps1` da por hecho que `.venv` ya existe. No lo crea.
- La detección de Ollama usa tres rutas conocidas y el PATH. Una instalación en otro sitio no se encontraría.
- La copia es manual y local. No hay copia automática ni fuera de F.
- El ZIP guarda una foto del momento: no sustituye al control de versiones ni conserva el historial.

### Siguiente paso, no iniciado
Queda pendiente decidir si se publica en GitHub todo lo acumulado desde `e7bc39d` y si se lleva una copia fuera de F.

## Publicación en GitHub del trabajo acumulado — 13 de septiembre de 2026 — Claude Code (Opus 5) en F

Ejecutado en F (DESKTOP-T6C436J), carpeta original. Único editor. Sin instalaciones y sin reescribir historial: no se ha usado `force push`.

### Comprobaciones previas a publicar
- Remoto `origin`: `https://github.com/interemprex/interemprex-ia-local.git`, que corresponde exactamente al repositorio indicado.
- Repositorio **privado** confirmado antes de publicar: `isPrivate: true`, `visibility: PRIVATE`, rama por defecto `main`.
- Cuenta autenticada: `interemprex`.
- `git fetch` previo: **cero commits remotos sin traer** y cero locales sin publicar. No había divergencia que integrar, así que no hizo falta ningún `merge` ni `rebase`.
- Barrido de secretos sobre lo que se iba a publicar (claves privadas, tokens `ghp_`/`gho_`/`github_pat`, claves AWS, contraseñas): sin coincidencias.
- Archivos ignorados, que **no** se han forzado a entrar: `.venv/`, `__pycache__/`, `data/` y `logs/`. Los ZIP de respaldo viven fuera del proyecto, así que Git ni los ve.

### Documentación actualizada antes del commit
- `README.md` reescrito para describir la primera versión de uso interno: arranque en un comando, qué programas hay, cómo funciona la consulta documental, qué es el modo literal y las limitaciones medidas. Se corrigió que seguía afirmando «Sin consulta documental integrada», que había dejado de ser cierto.
- `TRASPASO_CLAUDE.md`: se corrigió que los tres borradores «todavía no se consultan desde el chat». Ya se consultan; se añade que el fallo P3 sigue abierto y cómo se gestiona.
- No se añadieron funciones ni se reabrió la investigación de P3.

### Qué se publica
Código y scripts: `asistente_documental.py`, `consultar_documentos.py`, `chat_ollama.py`, `probar_ollama.py`, `comprobar_entorno.py`, `iniciar_asistente.ps1`, `crear_copia_seguridad.ps1`, `.gitignore`.
Documentación: `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTEXTO_NEGOCIO.md`, `ESTADO_PROYECTO.md`, `GUIA_CONTINUIDAD.md`, `TRASPASO_CLAUDE.md`.

### Qué queda deliberadamente fuera, y no es un fallo de publicación
`data/` entero, por decisión de diseño: los tres documentos de negocio, los registros de conversaciones de `data/asistente/` y `data/consultas/`, y las evidencias de las pruebas P0 de `data/pruebas/`. También `logs/`, `.venv`, `__pycache__` y los ZIP de respaldo.

Consecuencia que conviene tener presente: **los documentos de negocio y las evidencias de prueba no tienen respaldo en GitHub**. Su única copia está en F y en los ZIP locales, que están en el mismo disco.
