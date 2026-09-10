"""Primera consulta local: Python en F -> Ollama en F -> respuesta."""

import json
import platform
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def consultar(pregunta):
    # JSON es el formato de datos que enviamos a la API de Ollama.
    datos = {
        "model": "qwen3:8b",
        "messages": [
            {"role": "system", "content": "Responde en español de forma breve. No inventes datos sobre INTEREMPREX."},
            {"role": "user", "content": pregunta},
        ],
        "stream": False,  # Recibir la respuesta completa en una sola entrega.
        "think": False,   # Para esta prueba sencilla, desactivar el modo thinking.
        "options": {"num_ctx": 4096, "num_predict": 256},
    }
    peticion = Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(peticion, timeout=180) as respuesta:
        return json.load(respuesta)


def main():
    pregunta = " ".join(sys.argv[1:]) or "Explica en tres frases qué es una API y cómo conecta Python con un modelo local."
    print("Equipo:", platform.node())
    print("Python:", sys.executable)
    print("Pregunta:", pregunta)
    print("Esperando respuesta de Ollama...", flush=True)
    try:
        resultado = consultar(pregunta)
    except HTTPError as error:
        print(f"Ollama devolvió HTTP {error.code}: {error.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        return 1
    except (URLError, TimeoutError) as error:
        print(f"No se recibió respuesta. Comprueba que ollama serve sigue activo en F. Detalle: {error}", file=sys.stderr)
        return 1
    print("\nRespuesta:\n" + resultado["message"]["content"])
    if resultado.get("done_reason") == "length":
        print("\nLa respuesta alcanzó el límite de tokens de esta prueba.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
