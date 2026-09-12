# INTEREMPREX — IA local

Proyecto de aprendizaje y desarrollo de un asistente documental local con fuentes, seguido de integraciones con LeadFinder y CRM.

Todo se ejecuta en el equipo F (DESKTOP-T6C436J). El Mac es cliente remoto por VS Code Remote SSH; el equipo D se añadirá después. `localhost` siempre se refiere a la máquina donde corre el programa, que aquí es F.

## Referencias del proyecto
- ESTADO_PROYECTO.md: estado verificado y siguiente paso. Leer al comenzar cada sesión.
- GUIA_CONTINUIDAD.md: cómo arrancar cada día y cómo retomar tras apagar F.
- TRASPASO_CLAUDE.md: contexto de continuidad para Claude.
- CLAUDE.md y AGENTS.md: instrucciones de trabajo y coordinación entre asistentes.

## Arquitectura actual
MacBook Pro → Tailscale → OpenSSH → VS Code remoto en F → Python → Ollama → qwen3:8b.
Ollama 0.33.3 sirve en `127.0.0.1:11434` de F. Solo se usa la biblioteca estándar de Python: no hay dependencias que instalar.

## Programas
- `comprobar_entorno.py`: muestra equipo, intérprete y si se está dentro del entorno virtual.
- `probar_ollama.py`: una única consulta por ejecución. Sirve para comprobar que la cadena Python → API → modelo responde.
- `chat_ollama.py`: chat de terminal con historial durante la sesión.

## Uso
Requiere que Ollama esté sirviendo en F. Si no lo está, arrancarlo según GUIA_CONTINUIDAD.md.

```powershell
.\.venv\Scripts\python.exe comprobar_entorno.py
.\.venv\Scripts\python.exe probar_ollama.py "Explica qué es una variable en Python."
.\.venv\Scripts\python.exe chat_ollama.py
```

Dentro del chat: `/salir` termina, `/limpiar` olvida el historial. También salen Ctrl+C y Ctrl+D.
Cada turno imprime una línea `[contexto: N intercambios previos, ~M tokens estimados]` para que se vea qué se está enviando al modelo.

## Cómo funciona el historial del chat
El modelo no recuerda nada por sí mismo: en cada turno se le reenvía la conversación entera. `chat_ollama.py` guarda los intercambios de la sesión y aplica dos límites al construir cada petición:

1. **Número de turnos.** `MAX_INTERCAMBIOS = 8` **incluye el turno actual**, así que viajan como mucho 7 intercambios previos más la pregunta. Se descartan intercambios completos, nunca media pareja pregunta/respuesta.
2. **Tamaño.** Presupuesto de entrada = 4096 de contexto − 512 reservados para la respuesta − 128 de margen = 3456 tokens estimados. Si el historial no cabe, se sueltan intercambios enteros del más antiguo al más reciente.

Si una pregunta no cabe ni siquiera ella sola, se rechaza antes de enviarla indicando cuánto sobra, y no se guarda en el historial.

## Limitaciones actuales
Conviene tenerlas presentes antes de confiar en el chat:

- **Sin memoria entre sesiones.** Al cerrar el programa se pierde todo. No hay base de datos ni fichero de conversaciones.
- **Sin documentos ni fuentes.** Todavía no hay RAG: el chat no conoce ningún documento de INTEREMPREX y puede inventar si se le pregunta por ellos.
- **Olvida lo antiguo dentro de la propia sesión.** Comprobado: con 10 turnos, el turno 10 recordaba los turnos 3 a 9 y había perdido los dos primeros.
- **El recuento de tokens es una estimación, no una medida exacta.** No usa el tokenizador real del modelo. Frente al recuento real de qwen3:8b sobra margen con prosa (+35%) y falta con texto lleno de cifras (−19%). Si se queda corta, Ollama recorta el principio del prompt por su cuenta y el chat pierde memoria sin avisar.
- **Sin streaming.** La respuesta aparece de golpe tras `Pensando...`.
- **El historial crece en memoria** mientras dura la sesión; no está acotado.
- **Ollama no arranca solo.** Hay que lanzar `ollama serve` a mano en F y dejar esa terminal abierta. No hay encendido remoto de F ni acceso probado desde fuera de casa.

## Colaboración
Los archivos en disco son la referencia común. Los adjuntos de Claude web son copias que hay que actualizar a mano; no hay sincronización automática entre chats. Un solo asistente edita el árbol de trabajo a la vez y los demás revisan después.

Repositorio privado en GitHub: https://github.com/interemprex/interemprex-ia-local (cuenta `interemprex`). `.venv`, modelos, credenciales, claves y documentos privados quedan fuera del control de versiones mediante `.gitignore`.
