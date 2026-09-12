# Estado del proyecto — 2026-09-10

Responsable de esta actualización: Codex. Referencia actual para ambos asistentes. Este documento sustituye las notas de estado antiguas del README.

## Objetivo
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
