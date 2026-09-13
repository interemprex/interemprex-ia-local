# Traspaso a Claude — INTEREMPREX

Este documento es una síntesis operativa del chat, NO una transcripción literal ni un archivo con todas las imágenes. Leer ESTADO_PROYECTO.md para el estado actual y CLAUDE.md para reglas de trabajo.

## Intención del usuario
Aprender IA general, programación y aplicaciones locales construyendo infraestructura para INTEREMPREX. Explicar los pasos sin divagar. Interconectar Claude, Claude Code, Python, GitHub, VS Code y Ollama. F ejecutará la IA y permitirá acceso desde D y Mac; Mac es el cliente actual. Tener en cuenta acceso fuera de casa desde el principio.

## Visión
Contexto empresarial vigente, confirmado por el usuario el 2026-09-13: desarrollar aplicaciones a medida para negocios y su mantenimiento, incluyendo desarrollo web, automatización e internacionalización. Leer CONTEXTO_NEGOCIO.md. Esta definición sustituye el encuadre anterior de agencia genérica; no añadir marketing digital o ecommerce como líneas comerciales independientes sin confirmación.

Primer producto: consultar pocos documentos de INTEREMPREX con fuentes y reconocer información ausente. Evolución: RAG, CRM, LeadFinder, propuestas y automatizaciones verificadas. Flujo empresarial de referencia: LeadFinder → scoring → CRM → pipeline → propuesta → cliente → operación.

Empezar con inferencia de modelos entrenados. RAG recupera documentos, no modifica pesos. Ollama ejecuta modelos y sirve una API; herramientas, permisos y memoria persistente se programan en la aplicación. Claude Code tiene proveedor y autenticación independientes de Ollama.

qwen3:8b está descargado y probado tanto por CLI como por Python. Ollama 0.33.3 sirve en 127.0.0.1:11434 de F. ollama ps mostró 5.6 GB, 100% GPU y contexto 4096; esto indica ubicación del modelo, no porcentaje de utilización de GPU. qwen3:14b solo fue una propuesta, no está verificado como instalado. No se necesita fine-tuning al comenzar.

## Aprendizajes explicados
- Terminal nativa de Mac ejecuta en Mac, salvo sesión SSH. Terminal integrada de la ventana remota ejecuta en F. localhost depende de dónde corre el programa.
- Tailscale aporta conectividad; OpenSSH acceso; VS Code editor remoto.
- Clave pública en F; privada en cada cliente.
- .venv separa dependencias y no se versiona. sys.executable identifica el intérprete y sys.prefix != sys.base_prefix identifica el entorno virtual.
- Windows 10 era un dato antiguo de F; se corrigió a Windows 11 25H2. Evitar recuperar el dato obsoleto del historial.

## Colaboración
Claude Code implementa tareas delimitadas; Codex revisa después. Un solo asistente edita el mismo árbol de trabajo en cada momento. Leer y actualizar ESTADO_PROYECTO.md. Si trabajan en copias distintas, compartir commits mediante GitHub una vez configurado; requiere commit/push/pull.

Claude web requiere adjuntos actuales o integración comprobada. No tiene acceso automático a la carpeta de F, al chat de Codex ni a cambios de Claude Code. Archivos subidos son copias. No afirmar sincronización en tiempo real ni asumir que un enlace al chat permite leerlo entero.

## Mensaje inicial para Claude
Lee CONTEXTO_NEGOCIO.md, ESTADO_PROYECTO.md, CLAUDE.md, AGENTS.md y GUIA_CONTINUIDAD.md. Python, Ollama, el chat con historial y la publicación en GitHub están documentados; consulta el estado más reciente sin repetir instalaciones. El acceso de Claude Code a F ya fue verificado en la sesión anterior, pero identifica tu acceso real al retomar. Los tres borradores de negocio de data/documentos/ YA se consultan: consultar_documentos.py los busca y asistente_documental.py redacta sobre ellos, con el arranque unificado en iniciar_asistente.ps1. Sigue abierto el fallo P3, descrito en el estado: con procedimientos marcados como propuesta el modelo tiende a presentarlos como vigentes, y por eso esas consultas se entregan en texto literal sin pasar por el modelo. Explica cada paso, separa hechos y propuestas y actualiza el estado con resultados reales. Si solo dispones de adjuntos, trátalos como una copia estática.

