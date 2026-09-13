# INTEREMPREX — IA local

Asistente documental local para INTEREMPREX: responde preguntas sobre los documentos de la empresa mostrando siempre de dónde sale cada cosa. Proyecto de aprendizaje además de herramienta.

INTEREMPREX tiene como objetivo desarrollar aplicaciones a medida para negocios y su mantenimiento, incluyendo desarrollo web, automatización e internacionalización. CONTEXTO_NEGOCIO.md recoge la definición confirmada el 13 de septiembre de 2026.

Todo se ejecuta en el equipo F (DESKTOP-T6C436J). El Mac es cliente remoto por VS Code Remote SSH; el equipo D se añadirá después y **su acceso no está probado**. `localhost` siempre se refiere a la máquina donde corre el programa, que aquí es F.

## Estado: primera versión de uso interno
Funciona y se usa, pero no es un producto. Los documentos que consulta son **borradores** y sus límites están descritos más abajo sin adornos. No debe usarse como fuente de condiciones comerciales.

## Arranque diario
Un solo comando, en la terminal PowerShell de F (vale la remota de VS Code):

```powershell
.\iniciar_asistente.ps1
```

Comprueba el entorno, reutiliza Ollama si ya responde o lo arranca en segundo plano si no, y abre el asistente. Al salir con `/salir`, Ollama queda activo para la siguiente consulta. La secuencia completa del día está en GUIA_CONTINUIDAD.md.

## Referencias del proyecto
- ESTADO_PROYECTO.md: estado verificado y siguiente paso. Leer al comenzar cada sesión.
- CONTEXTO_NEGOCIO.md: objetivo empresarial vigente y alcance confirmado.
- GUIA_CONTINUIDAD.md: arranque diario y cómo retomar tras apagar F.
- TRASPASO_CLAUDE.md: contexto de continuidad para Claude.
- CLAUDE.md y AGENTS.md: instrucciones de trabajo y coordinación entre asistentes.

## Arquitectura actual
MacBook Pro → Tailscale → OpenSSH → VS Code remoto en F → Python → Ollama → qwen3:8b.
Ollama 0.33.3 sirve en `127.0.0.1:11434` de F. Solo biblioteca estándar de Python: no hay dependencias que instalar.

## Programas
- `iniciar_asistente.ps1`: arranque en un comando.
- `crear_copia_seguridad.ps1`: ZIP fechado de respaldo, fuera del proyecto.
- `asistente_documental.py`: el asistente. Busca los fragmentos pertinentes y pide al modelo una respuesta apoyada solo en ellos.
- `consultar_documentos.py`: solo búsqueda, sin modelo. Útil si Ollama no está disponible.
- `chat_ollama.py`: chat de terminal con historial de sesión, anterior a la consulta documental. Se conserva.
- `probar_ollama.py`: una consulta suelta, para comprobar que la cadena responde.
- `comprobar_entorno.py`: identifica equipo, intérprete y entorno virtual.

Si se prefiere lanzarlos a mano:

```powershell
.\.venv\Scripts\python.exe asistente_documental.py
.\.venv\Scripts\python.exe consultar_documentos.py
```

## Cómo funciona la consulta documental
Los tres documentos de `data/documentos/` se parten en secciones: 23 en total. Cada sección conserva su identificador, versión, estado y número, leídos de la cabecera del archivo.

1. **Busca** la sección más parecida a la pregunta, puntuando al estilo BM25: los términos comunes pesan poco, repetir suma cada vez menos y coincidir en el título de la sección vale el triple. Es coincidencia de **palabras, no de significado**.
2. **Entrega al modelo** hasta tres secciones, con su estado por delante del texto. Si una sección no cabe entera en el contexto, se descarta completa: nunca se corta, porque partirla podría dejar fuera la condición que matiza el resto.
3. **Muestra** la respuesta, los **Fragmentos consultados** con su procedencia y el **texto literal** de cada uno para contrastar.

La procedencia la añade el programa, no el modelo. En las pruebas se comprobó que el modelo reproduce mal los identificadores y las versiones, así que se le prohíbe escribir referencias.

### Modo literal
Si entre las secciones encontradas hay un **procedimiento pendiente de aprobación**, el programa **no llama al modelo**: muestra el texto original con su estado y explica por qué. El motivo es un fallo comprobado: al reformular esas secciones, el modelo tiende a presentarlas como la forma de trabajar vigente, y no lo son.

La regla es deliberadamente prudente. Se activa aunque solo una de las secciones encontradas sea una propuesta y aunque esa sección sea poco pertinente.

## Limitaciones conocidas
Medidas, no supuestas:

- **Hoy la mayoría de consultas no se redactan.** Siete de las 23 secciones son procedimientos propuestos, y en una batería de 10 preguntas el modo literal se activó en 7. Es el lado seguro del error, pero conviene saberlo: a menudo se comporta como un buscador con explicación.
- **La búsqueda compara palabras, no significados.** Si preguntas con un sinónimo que el documento no usa, no encuentra nada. Cuando no hay resultados, muestra el índice de secciones para poder ir directo.
- **Un resultado no es una respuesta.** La puntuación mide parecido de palabras: una puntuación alta puede acompañar a un fragmento que no sirve.
- **«No encontrado» no es una negativa comercial.** Que algo no esté escrito en tres borradores no significa que INTEREMPREX no lo ofrezca.
- **Solo se envían hasta tres secciones.** Una respuesta repartida entre más documentos quedará incompleta sin avisar.
- **Sin historial**: cada pregunta parte de cero.
- **El recuento de tokens es una estimación.** No usa el tokenizador real; sobreestima alrededor de un 24%, que es el lado seguro.
- **Ollama no arranca solo tras reiniciar Windows.** `iniciar_asistente.ps1` hay que lanzarlo a mano. No hay servicio, ni tarea programada, ni encendido remoto de F, ni acceso probado desde fuera de casa.
- **Los documentos son borradores** en versión 0.2, con decisiones comerciales sin resolver.

## Copia de seguridad
```powershell
.\crear_copia_seguridad.ps1
```
Genera un ZIP fechado en `C:\Users\Fer\Documents\Copias-INTEREMPREX`, fuera del proyecto, con código, documentación y los documentos de negocio. Incluye un inventario. Quedan fuera `.venv`, modelos, cachés, registros y conversaciones.

Protege frente a cambios o borrados accidentales. **No protege frente a una avería de F**: está en el mismo disco.

## Colaboración
Los archivos en disco son la referencia común. Los adjuntos de Claude web son copias que hay que actualizar a mano; no hay sincronización automática entre chats. Un solo asistente edita el árbol de trabajo a la vez y los demás revisan después.

Repositorio privado en GitHub: https://github.com/interemprex/interemprex-ia-local (cuenta `interemprex`). Quedan fuera del control de versiones, mediante `.gitignore`: `.venv`, `data/` (documentos de negocio, conversaciones y evidencias de prueba), `logs/`, cachés, modelos y credenciales.
