"""Asistente documental de INTEREMPREX: buscador local + qwen3:8b en Ollama.

Une dos piezas que ya funcionaban por separado:
- consultar_documentos.py elige las secciones pertinentes y aporta su procedencia.
- Ollama redacta una respuesta breve APOYADA SOLO en esas secciones.

Lo que se muestra siempre, en este orden: la respuesta, los fragmentos que se
entregaron al modelo con su procedencia leida por codigo, y el texto literal de
cada uno para poder contrastar. La procedencia NO la escribe el modelo: la
prueba P0 demostro que reproduce mal los metadatos.

FALLO P3, DOCUMENTADO Y ABIERTO: con secciones marcadas como "Propuesta:" el
modelo tiende a redactarlas como si fueran el procedimiento vigente. Mientras no
se resuelva, la decision se toma ANTES de generar: si entre los fragmentos
seleccionados hay un procedimiento pendiente de aprobacion, no se llama al
modelo y se entrega el texto literal con su estado. Es una regla conservadora;
ver aviso_modo_literal().

Cada pregunta es independiente: no hay historial todavia.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:  # sin esto los acentos se corrompen al redirigir entrada o salida en Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

import consultar_documentos as buscador   # se reutiliza tal cual
import chat_ollama as chat                # solo se lee estimar_tokens; no se modifica

URL = "http://127.0.0.1:11434/api/chat"
MODELO = "qwen3:8b"
NUM_CTX = 4096
NUM_PREDICT = 400
MARGEN_TOKENS = 128
PRESUPUESTO = NUM_CTX - NUM_PREDICT - MARGEN_TOKENS

MAX_FRAGMENTOS = 3
CARPETA_REGISTRO = RAIZ / "data" / "asistente"
SALIDAS = buscador.SALIDAS

AVISO_PROPUESTA = "PROCEDIMIENTO PROPUESTO"

# Nota de diseño: NO se le da al modelo una frase literal de negativa. En la
# prueba P0 v1 se comprobó que una cadena exacta lista para copiar compite con
# las reglas abstractas y gana; la primera version de este archivo repitio ese
# error y el modelo se nego a responder una pregunta que los fragmentos si
# respondian. Por eso la regla 1 es afirmativa y la negativa queda condicionada.
INSTRUCCIONES = """Eres un asistente documental de INTEREMPREX. Respondes usando ÚNICAMENTE los fragmentos que se te entregan más abajo.

1. Si alguno de los fragmentos trata el asunto de la pregunta, RESPÓNDELO con lo que dice, aunque sea una condición y no una cifra. No te niegues a responder porque falte un dato concreto: responde con lo que sí consta y señala qué parte no está definida.

2. CONSERVA el estatus con el que el documento presenta cada cosa: propuesta, alcance propuesto, entregables propuestos, pendiente de acuerdo, pendiente de definir, no aprobado en este borrador, no incluido automáticamente. No lo presentes como hecho consolidado ni como imposibilidad.

3. Solo si ningún fragmento trata el asunto, dilo abiertamente. Al hacerlo, limita lo que afirmes a los fragmentos que tienes delante: NO digas que algo falta en los documentos ni que no está en ninguna parte, porque solo has recibido algunas secciones sueltas y no sabes qué dicen las demás. No completes la respuesta con conocimiento tuyo ni con lo que sepas de otras empresas. Y no lo conviertas en una negativa: que no aparezca en estos fragmentos no significa que INTEREMPREX no lo ofrezca.

4. NO escribas referencias de ninguna clase: ni identificadores, ni versiones, ni números de sección, ni citas entre paréntesis. La procedencia se añade por separado y no es cosa tuya.

Responde en español, de forma breve pero completa. La brevedad nunca justifica omitir una condición que el documento establece."""


def preparar(pregunta, resultados):
    """Elige cuantos fragmentos caben en el presupuesto SIN partir ninguno.

    Si una seccion no cabe entera se descarta completa. Cortarla podria dejar
    fuera justo la condicion que matiza lo que dice el resto.
    """
    cabecera = "PREGUNTA: {}\n\nFRAGMENTOS:\n".format(pregunta)
    base = chat.estimar_tokens([{"role": "system", "content": INSTRUCCIONES},
                                {"role": "user", "content": cabecera}])
    incluidos, omitidos = [], []
    acumulado = base

    for r in resultados[:MAX_FRAGMENTOS]:
        f = r["fragmento"]
        bloque = bloque_para_modelo(f)
        coste = chat.estimar_tokens([{"role": "user", "content": bloque}])
        if acumulado + coste <= PRESUPUESTO:
            incluidos.append(r)
            acumulado += coste
        else:
            omitidos.append((r, coste))

    cuerpo = cabecera + "\n\n".join(bloque_para_modelo(r["fragmento"]) for r in incluidos)
    return incluidos, omitidos, cuerpo, acumulado


def bloque_para_modelo(f):
    """Fragmento tal como lo ve el modelo: estado por delante y texto literal."""
    avisos = buscador.avisos_de_contenido(f)
    partes = ["--- Sección «{}» ---".format(f["titulo"]),
              "Estado del documento: {}".format(f["estado"])]
    if avisos:
        partes.append("Avisos sobre esta sección: {}".format("; ".join(avisos)))
    partes.append(f["texto"])
    return "\n".join(partes)


def consultar_modelo(cuerpo):
    datos = {
        "model": MODELO,
        "messages": [{"role": "system", "content": INSTRUCCIONES},
                     {"role": "user", "content": cuerpo}],
        "stream": False,
        "think": False,
        "options": {"num_ctx": NUM_CTX, "num_predict": NUM_PREDICT, "temperature": 0.2},
    }
    peticion = Request(URL, data=json.dumps(datos).encode("utf-8"),
                       headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(peticion, timeout=300) as r:
        return json.load(r)


def procedimientos_propuestos(incluidos):
    """Fragmentos seleccionados que el documento marca como procedimiento propuesto."""
    return [r["fragmento"] for r in incluidos
            if AVISO_PROPUESTA in "; ".join(buscador.avisos_de_contenido(r["fragmento"]))]


def aviso_modo_literal(propuestos):
    """Explicacion que sustituye a la respuesta redactada.

    REGLA CONSERVADORA, a proposito: basta con que UNO de los fragmentos
    seleccionados sea un procedimiento propuesto para no llamar al modelo, aunque
    ese fragmento sea poco pertinente para la pregunta y los demas si lo sean.
    Se prefiere mostrar texto literal de mas a redactar de menos, porque el fallo
    P3 (presentar una propuesta como procedimiento vigente) sigue sin resolverse.
    """
    referencias = ", ".join("{} §{} «{}»".format(f["id"], f["seccion"], f["titulo"])
                            for f in propuestos)
    return (
        "No se ha redactado una respuesta para esta pregunta. Se muestra el texto original.\n"
        "\n"
        "Motivo: entre las secciones encontradas hay un procedimiento todavía PENDIENTE DE\n"
        "APROBACIÓN ({}).\n"
        "Redactarlo con otras palabras podría presentarlo como la forma de trabajar vigente,\n"
        "y no lo es. Por eso se entrega tal cual está escrito, con su marca «Propuesta:».\n"
        "\n"
        "La regla es deliberadamente prudente: se aplica aunque solo una de las secciones\n"
        "encontradas sea una propuesta, y aunque esa sección resulte poco pertinente."
    ).format(referencias)


def mostrar_fragmentos(incluidos, omitidos, total_encontrados):
    lineas = []
    lineas.append("")
    lineas.append("=" * 78)
    lineas.append("FRAGMENTOS CONSULTADOS — {} de {} secciones encontradas".format(
        len(incluidos), total_encontrados))
    lineas.append("Procedencia añadida por el programa desde la cabecera de cada archivo.")
    lineas.append("Son los fragmentos que se entregaron al modelo, NO afirmaciones verificadas:")
    lineas.append("que una sección se consultara no significa que respalde la respuesta.")
    lineas.append("=" * 78)

    for i, r in enumerate(incluidos, 1):
        f = r["fragmento"]
        avisos = buscador.avisos_de_contenido(f)
        lineas.append("")
        lineas.append("[{}] {} · versión {} · sección {} · «{}»".format(
            i, f["id"], f["version"], f["seccion"], f["titulo"]))
        lineas.append("    Archivo: {}".format(f["archivo"]))
        lineas.append("    ESTADO DEL DOCUMENTO: {}".format(f["estado"]))
        if avisos:
            lineas.append("    AVISOS SOBRE ESTA SECCIÓN: {}".format("; ".join(avisos)))
        lineas.append("    Coincide en: {} (puntuación {:.2f}; mide parecido de palabras,".format(
            ", ".join(r["coincidencias"]), r["puntos"]))
        lineas.append("    no que el fragmento responda a la pregunta)")
        lineas.append("")
        lineas.append("    TEXTO LITERAL, para contrastar la respuesta:")
        lineas.append("    " + "." * 70)
        for linea in f["texto"].splitlines():
            lineas.append("    " + linea)
        lineas.append("    " + "." * 70)

    for r, coste in omitidos:
        f = r["fragmento"]
        lineas.append("")
        lineas.append("[omitido] {} §{} «{}»: no cabía entero en el contexto (~{} tokens).".format(
            f["id"], f["seccion"], f["titulo"], coste))
        lineas.append("          Se descarta completo antes que cortarlo por la mitad.")
    return "\n".join(lineas)


def main():
    fragmentos, avisos_carga = buscador.cargar()
    for aviso in avisos_carga:
        print("AVISO: {}".format(aviso), file=sys.stderr)
    if not fragmentos:
        print("No hay documentos que consultar.", file=sys.stderr)
        return 1
    indice = buscador.construir_indice(fragmentos)

    print("Asistente documental de INTEREMPREX")
    print("{} secciones indexadas. Modelo {} en {}".format(len(fragmentos), MODELO, URL))
    print("Presupuesto de entrada: ~{} tokens estimados de {} de contexto.".format(
        PRESUPUESTO, NUM_CTX))
    print("Cada pregunta es independiente: no se recuerda la anterior. /salir para terminar.")

    registro = ["# Sesión del asistente documental — {:%Y-%m-%d %H:%M}".format(datetime.now()),
                "", "Equipo F (DESKTOP-T6C436J). Modelo {}, num_ctx {}, num_predict {}.".format(
                    MODELO, NUM_CTX, NUM_PREDICT), ""]
    hubo = False

    while True:
        try:
            pregunta = input("\nPregunta: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nFin de la sesión.")
            break
        if not pregunta:
            continue
        if pregunta.lower() in SALIDAS:
            print("Fin de la sesión.")
            break

        hubo = True
        registro.append("## Pregunta: {}".format(pregunta))
        resultados, tokens = buscador.buscar(pregunta, fragmentos, indice)

        if not resultados:
            texto = buscador.mensaje_sin_resultados(tokens, fragmentos)
            print("\nNo se consulta al modelo: no hay fragmentos en los que apoyarse.\n")
            print(texto)
            registro.append("SIN FRAGMENTOS. No se llamó al modelo.")
            registro.append(texto)
            registro.append("")
            continue

        incluidos, omitidos, cuerpo, estimados = preparar(pregunta, resultados)
        if not incluidos:
            print("\nNinguna sección cabe entera en el contexto disponible. No se consulta")
            print("al modelo: cortar una sección podría dejar fuera una condición.")
            registro.append("Ningún fragmento cabía entero. No se llamó al modelo.")
            continue

        # Decision ANTES de generar: si hay un procedimiento propuesto entre los
        # fragmentos, no se llama al modelo. Vale mas no redactar que redactar
        # convirtiendo una propuesta en procedimiento vigente.
        propuestos = procedimientos_propuestos(incluidos)
        if propuestos:
            bloque = mostrar_fragmentos(incluidos, omitidos, len(resultados))
            print("\n" + "=" * 78)
            print("MODO LITERAL — no se ha consultado al modelo")
            print("=" * 78)
            print(aviso_modo_literal(propuestos))
            print(bloque)
            registro.append("MODO LITERAL: no se llamó al modelo.")
            registro.append("Procedimientos propuestos entre los fragmentos: {}".format(
                ", ".join("{} §{}".format(f["id"], f["seccion"]) for f in propuestos)))
            registro.append("")
            registro.append("### Fragmentos consultados")
            registro.append(bloque)
            registro.append("")
            continue

        print("\nConsultando a qwen3:8b con {} fragmento(s)...".format(len(incluidos)), flush=True)
        try:
            res = consultar_modelo(cuerpo)
        except (URLError, TimeoutError) as e:
            print("\nNo hay respuesta de Ollama. ¿Está 'ollama serve' activo en F?", file=sys.stderr)
            print("Arráncalo con:  & \"$env:LOCALAPPDATA\\Programs\\Ollama\\ollama.exe\" serve",
                  file=sys.stderr)
            print("Detalle: {}".format(e), file=sys.stderr)
            print("\nLos fragmentos encontrados sí están disponibles:")
            print(mostrar_fragmentos(incluidos, omitidos, len(resultados)))
            registro.append("ERROR de conexión con Ollama: {}".format(e))
            continue
        except HTTPError as e:
            print("\nOllama devolvió HTTP {}: {}".format(
                e.code, e.read().decode("utf-8", errors="replace")), file=sys.stderr)
            registro.append("ERROR HTTP de Ollama.")
            continue

        cruda = res["message"]["content"].strip()
        reales = res.get("prompt_eval_count")

        print("\n" + "=" * 78)
        print("RESPUESTA — basada únicamente en los fragmentos consultados")
        print("=" * 78)
        print(cruda)
        bloque = mostrar_fragmentos(incluidos, omitidos, len(resultados))
        print(bloque)
        print("")
        print("Contexto: ~{} tokens estimados frente a {} reales de entrada.".format(
            estimados, reales))

        registro.append("Fragmentos entregados: {}".format(
            ", ".join("{} §{}".format(r["fragmento"]["id"], r["fragmento"]["seccion"])
                      for r in incluidos)))
        registro.append("Tokens estimados {} / reales {}".format(estimados, reales))
        registro.append("")
        registro.append("### Respuesta original del modelo, sin retocar")
        registro.append(cruda)
        registro.append("")
        registro.append("### Fragmentos consultados")
        registro.append(bloque)
        registro.append("")

    if hubo:
        CARPETA_REGISTRO.mkdir(parents=True, exist_ok=True)
        destino = CARPETA_REGISTRO / "sesion_{:%Y-%m-%d_%H%M%S}.md".format(datetime.now())
        destino.write_text("\n".join(registro), encoding="utf-8")
        print("\nRegistro de la sesión guardado en: {}".format(destino))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
