"""Chat de terminal: Python en F -> Ollama en F -> qwen3:8b, con historial de sesion."""

import json
import platform
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

URL = "http://127.0.0.1:11434/api/chat"
MODELO = "qwen3:8b"
SISTEMA = "Responde en español de forma breve y clara. No inventes datos sobre INTEREMPREX."

NUM_CTX = 4096
NUM_PREDICT = 512

# Cuenta el turno actual: viajan como mucho MAX_INTERCAMBIOS - 1 intercambios
# completos anteriores, mas la pregunta pendiente.
MAX_INTERCAMBIOS = 8

# Presupuesto para la entrada: el contexto menos la respuesta reservada y un margen
# para la plantilla de chat que Ollama añade por su cuenta.
MARGEN_TOKENS = 128
PRESUPUESTO_ENTRADA = NUM_CTX - NUM_PREDICT - MARGEN_TOKENS

CHARS_POR_TOKEN = 3.5
COSTE_POR_MENSAJE = 4

SALIDAS = {"/salir", "salir", "/exit", "exit", "/quit", "quit"}


def estimar_tokens(mensajes):
    """Estimacion aproximada del tamaño de la entrada, NO un recuento exacto.

    Texto corriente: unos 3,5 caracteres por token. Cifras y simbolos se cuentan
    como un token cada uno, porque el tokenizador los parte mucho mas fino.

    Error medido contra prompt_eval_count real de qwen3:8b el 2026-09-10:
    prosa +35%, URLs +39%, codigo +7%, cifras -19%, frase corta -17%.
    Es decir, tiende a sobrar margen con texto normal y a quedarse corta con
    cifras. No es una garantia: si se queda corta, Ollama recorta el principio
    del prompt por su cuenta y el chat pierde memoria en silencio. Por eso
    existe MARGEN_TOKENS.
    """
    total = 0
    for mensaje in mensajes:
        texto = mensaje["content"]
        densos = sum(1 for c in texto if not c.isalpha() and not c.isspace())
        total += densos + int((len(texto) - densos) / CHARS_POR_TOKEN) + COSTE_POR_MENSAJE
    return total


def preparar_peticion(completos, pregunta):
    """Construye los mensajes a enviar aplicando el limite de turnos y el de tamaño.

    completos: lista plana de intercambios ya cerrados, siempre en pares
    usuario+asistente y sin mensaje de sistema.

    Descarta intercambios enteros, nunca medio par, para que la conversacion
    enviada nunca empiece por una respuesta sin su pregunta.

    Devuelve (mensajes, intercambios_previos), o (None, 0) si la pregunta no cabe
    ni siquiera sola.
    """
    sistema = {"role": "system", "content": SISTEMA}
    nuevo = {"role": "user", "content": pregunta}

    if estimar_tokens([sistema, nuevo]) > PRESUPUESTO_ENTRADA:
        return None, 0

    tope = (MAX_INTERCAMBIOS - 1) * 2
    recientes = completos[-tope:] if tope else []

    while recientes and estimar_tokens([sistema] + recientes + [nuevo]) > PRESUPUESTO_ENTRADA:
        recientes = recientes[2:]

    return [sistema] + recientes + [nuevo], len(recientes) // 2


def consultar(mensajes):
    datos = {
        "model": MODELO,
        "messages": mensajes,
        "stream": False,
        "think": False,
        "options": {"num_ctx": NUM_CTX, "num_predict": NUM_PREDICT},
    }
    peticion = Request(
        URL,
        data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(peticion, timeout=180) as respuesta:
        return json.load(respuesta)


def main():
    print("Equipo:", platform.node())
    print("Python:", sys.executable)
    print(f"Modelo: {MODELO} en {URL}")
    print(f"Contexto {NUM_CTX}: hasta ~{PRESUPUESTO_ENTRADA} tokens estimados de entrada"
          f" y {NUM_PREDICT} reservados para la respuesta.")
    print(f"Historial: {MAX_INTERCAMBIOS} intercambios contando el actual"
          f" ({MAX_INTERCAMBIOS - 1} previos). /salir para terminar, /limpiar para olvidar.")

    # Historial completo de la sesion, en pares cerrados. El limite se aplica al
    # construir cada peticion, asi que una pregunta larga puntual no borra nada.
    completos = []

    while True:
        try:
            pregunta = input("\nTu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nFin de la sesion.")
            return 0

        if not pregunta:
            continue
        if pregunta.lower() in SALIDAS:
            print("Fin de la sesion.")
            return 0
        if pregunta.lower() == "/limpiar":
            completos = []
            print("Historial borrado.")
            continue

        mensajes, previos = preparar_peticion(completos, pregunta)
        if mensajes is None:
            solos = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": pregunta}]
            sobra = estimar_tokens(solos) - PRESUPUESTO_ENTRADA
            print(
                f"Pregunta demasiado larga: sobran ~{sobra} tokens estimados"
                f" (~{int(sobra * CHARS_POR_TOKEN)} caracteres). Acortala o dividela en partes.",
                file=sys.stderr,
            )
            continue

        print(f"[contexto: {previos} intercambios previos, ~{estimar_tokens(mensajes)} tokens estimados]")
        print("Pensando...", flush=True)
        try:
            resultado = consultar(mensajes)
        except HTTPError as error:
            detalle = error.read().decode("utf-8", errors="replace")
            print(f"Ollama devolvio HTTP {error.code}: {detalle}", file=sys.stderr)
            continue
        except (URLError, TimeoutError) as error:
            print(
                "Sin respuesta de Ollama. Comprueba que 'ollama serve' sigue activo en F.\n"
                f"Detalle: {error}",
                file=sys.stderr,
            )
            continue

        contenido = resultado["message"]["content"]
        # El par solo se cierra cuando la respuesta llega bien, para que el
        # historial no acumule preguntas sin contestar.
        completos.append({"role": "user", "content": pregunta})
        completos.append({"role": "assistant", "content": contenido})

        print(f"\n{MODELO}: {contenido}")
        if resultado.get("done_reason") == "length":
            print("(La respuesta alcanzo el limite de tokens de este chat.)")


if __name__ == "__main__":
    raise SystemExit(main())
