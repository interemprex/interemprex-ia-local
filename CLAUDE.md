# Instrucciones del proyecto

Desarrollar un asistente local para INTEREMPREX y enseñar al usuario los fundamentos mientras se construye.

Contexto empresarial confirmado por el usuario el 2026-09-13: INTEREMPREX tiene como objetivo desarrollar aplicaciones a medida para negocios y su mantenimiento, incluyendo desarrollo web, automatización e internacionalización. Leer CONTEXTO_NEGOCIO.md; esta definición prevalece sobre las descripciones comerciales anteriores. Los entregables, tarifas y condiciones no aprobados deben tratarse como propuestas o pendientes.

- Explicar brevemente qué se cambia, para qué sirve y cómo se comprueba.
- Trabajar en pasos pequeños y verificables, manteniendo el objetivo documental inicial.
- Preferencia explícita del usuario: antes de una fase que requiera especial dedicación, esfuerzo o razonamiento complejo, mostrar «Recomendación: usar un modelo avanzado de IA» y explicar brevemente el motivo. No hace falta este aviso para comprobaciones sencillas. No afirmar que se ha cambiado de modelo automáticamente.
- F es el equipo previsto de ejecución; D debe poder acceder remotamente. Confirmar siempre en qué máquina se ejecuta un comando.
- Mantener Python y Ollama juntos en F; Mac es el cliente remoto actual mediante VS Code Remote SSH. D se añadirá después.
- No confundir localhost de D con localhost de F.
- No afirmar que una conexión, instalación o prueba funciona sin comprobarla.
- Guardar decisiones y estado en archivos del repositorio. No asumir memoria compartida entre Claude web, Claude Code y el modelo local.
- Mantener credenciales, documentos privados, pesos de modelos y .venv fuera de Git.
- Usar Ollama para inferencia local. Claude Code utiliza una autenticación/proveedor independiente; no asumir ejecución local de Claude.
- Antes de enviar información privada a servicios externos, determinar los datos necesarios y la autorización existente.
- Empezar con herramientas de lectura. Validar argumentos y resultados antes de incorporar escrituras externas.
- Posponer agentes múltiples, fine-tuning e infraestructura adicional hasta que una necesidad comprobada los justifique.
- Leer ESTADO_PROYECTO.md al comenzar y actualizarlo al terminar con pruebas y siguiente paso. Consultar AGENTS.md para coordinación. Un solo asistente edita el mismo árbol a la vez.
