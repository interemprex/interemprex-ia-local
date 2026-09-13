"""Consulta documental de INTEREMPREX: busca fragmentos y los muestra literales.

Primera version utilizable. Busca en los tres documentos de data/documentos/ sin
que haya que elegir antes el documento correcto, y devuelve las secciones mas
parecidas a la pregunta, con su procedencia.

Que hace y que NO hace:
- SI: localiza secciones, muestra su texto EXACTO y anade la procedencia
  (identificador, version, estado, seccion) leida por codigo de la cabecera.
- NO: no resume, no parafrasea y no consulta ningun modelo de lenguaje. La
  prueba P0 mostro que el modelo pierde el caracter de propuesta de algunos
  procedimientos, asi que en esta version el texto se entrega sin intermediario.
  Integrar la respuesta del modelo es un paso posterior, que se apoyara en esto.

Busqueda por coincidencia de palabras, con la biblioteca estandar. No hay
base de datos, ni indice persistente, ni modelo de embeddings.
"""

import re
import sys
import unicodedata
from datetime import datetime
from math import log
from pathlib import Path

# La codificacion por defecto en Windows es cp1252. La consola interactiva
# funciona igualmente, pero en cuanto se redirige la entrada o la salida (por
# ejemplo para automatizar una prueba) los acentos se corrompen: "internacional-
# izacion" llegaba a la busqueda como "internacionalizacia" y no encontraba nada.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

RAIZ = Path(__file__).resolve().parent
CARPETA_DOCS = RAIZ / "data" / "documentos"
CARPETA_REGISTRO = RAIZ / "data" / "consultas"

RESULTADOS = 3          # cuantos fragmentos se muestran por pregunta
SALIDAS = {"/salir", "salir", "/exit", "exit", "/quit", "quit"}

# Parametros de la puntuacion, al estilo BM25, que es la formula clasica de
# busqueda por palabras. K1 controla cuanto deja de sumar cada repeticion de un
# termino; B, cuanto se penaliza que una seccion sea larga; PESO_TITULO, cuanto
# vale que la palabra buscada este en el titulo de la seccion. Son valores
# habituales, ajustados a mano sobre estos documentos.
K1 = 1.5
B = 0.75
PESO_TITULO = 3
UMBRAL_DEBIL = 1.0      # por debajo de esto se avisa de que la coincidencia es floja

# Palabras que aparecen en casi cualquier frase y no ayudan a distinguir secciones.
VACIAS = {
    "de", "la", "el", "los", "las", "un", "una", "unos", "unas", "y", "o", "a", "en",
    "que", "se", "del", "al", "por", "para", "con", "su", "sus", "es", "son", "lo",
    "como", "mas", "este", "esta", "esto", "estos", "estas", "ese", "esa", "esos",
    "esas", "hay", "ha", "han", "he", "cual", "cuales", "quien", "quienes", "donde",
    "cuando", "cuanto", "cuanta", "cuantos", "cuantas", "si", "no", "ni", "pero",
    "ya", "muy", "tambien", "sobre", "entre", "ser", "tiene", "tienen", "hacer",
    "puede", "pueden", "debe", "deben", "cada", "todo", "toda", "todos", "todas",
    "me", "te", "le", "les", "nos", "yo", "tu", "el", "ella", "mi", "sin", "hasta",
    "desde", "entonces", "porque", "entonces", "algun", "alguna", "algunos",
    # El nombre de la empresa es el sujeto de los tres documentos: aparece en
    # todos y no sirve para distinguir una seccion de otra. Si se deja, una
    # pregunta como "¿que automatizacion ofrece INTEREMPREX?" puede acabar
    # premiando una seccion generica que lo repite mucho, por encima de la
    # seccion que trata realmente de automatizacion. Comprobado al construirlo.
    "interemprex",
}

# Marcas que el propio documento usa para calificar su contenido. Se detectan en el
# texto literal y se avisan ANTES de mostrarlo, para que nadie lea una propuesta
# como si fuera una condicion acordada.
MARCAS = [
    (r"^Propuesta:", "PROCEDIMIENTO PROPUESTO, pendiente de aprobación"),
    (r"Alcance propuesto", "alcance propuesto, no acordado"),
    (r"Entregables propuestos", "entregables propuestos, no acordados"),
    (r"Modalidades propuestas", "modalidades propuestas, no acordadas"),
    (r"Pendiente de acuerdo", "contiene puntos pendientes de acuerdo"),
    (r"Pendiente de definir", "contiene puntos pendientes de definir"),
    (r"pendientes de definir", "contiene puntos pendientes de definir"),
    (r"Objetivo confirmado", "contiene objetivos confirmados"),
    (r"Ámbito confirmado", "contiene ámbitos confirmados"),
    (r"Resultado esperado", "describe un resultado esperado, no garantizado"),
]


def normalizar(texto):
    """Minusculas, sin acentos: 'Automatización' y 'automatizacion' deben coincidir."""
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def raiz_simple(palabra):
    """Recorte de plural muy basico. No es un lematizador; ver LIMITACIONES."""
    if len(palabra) > 5 and palabra.endswith("es"):
        return palabra[:-2]
    if len(palabra) > 4 and palabra.endswith("s"):
        return palabra[:-1]
    return palabra


def tokenizar(texto):
    palabras = re.findall(r"[a-z0-9]+", normalizar(texto))
    return [raiz_simple(p) for p in palabras if len(p) >= 3 and p not in VACIAS]


def metadatos(texto, nombre):
    """Lee ID, version y estado de la cabecera. No inventa: informa si faltan."""
    campos = {
        "id": re.findall(r"^ID:[ \t]*(\S+)[ \t]*$", texto, re.M),
        "version": re.findall(r"^Versión:[ \t]*(\S+)[ \t]*$", texto, re.M),
        "estado": re.findall(r"^Estado:[ \t]*(.+?)[ \t]*$", texto, re.M),
    }
    errores = []
    for campo, valores in campos.items():
        if not valores:
            errores.append("falta '{}' en la cabecera de {}".format(campo, nombre))
        elif len(valores) > 1:
            errores.append("'{}' ambiguo en {}: {}".format(campo, nombre, valores))
    if errores:
        return None, errores
    return {k: v[0] for k, v in campos.items()}, []


def cargar():
    """Devuelve (fragmentos, avisos). Un fragmento es una seccion de un documento."""
    fragmentos, avisos = [], []
    if not CARPETA_DOCS.is_dir():
        return [], ["No existe la carpeta {}".format(CARPETA_DOCS)]

    for ruta in sorted(CARPETA_DOCS.glob("*.md")):
        # UTF-8 explicito: la codificacion por defecto de Windows es cp1252 y
        # leer estos archivos sin indicarlo falla con UnicodeDecodeError.
        texto = ruta.read_text(encoding="utf-8")
        meta, errores = metadatos(texto, ruta.name)
        if errores:
            avisos.extend(errores)
            avisos.append("Se omite {}: sin metadatos fiables no se puede citar.".format(ruta.name))
            continue

        titulo_doc = texto.splitlines()[0].lstrip("# ").strip()
        actual = None
        for linea in texto.splitlines():
            cabecera = re.match(r"^##\s*(\d+)\.\s*(.+)$", linea)
            if cabecera:
                actual = {
                    "archivo": ruta.name,
                    "titulo_documento": titulo_doc,
                    "id": meta["id"],
                    "version": meta["version"],
                    "estado": meta["estado"],
                    "seccion": int(cabecera.group(1)),
                    "titulo": cabecera.group(2).strip(),
                    "lineas": [],
                }
                fragmentos.append(actual)
            elif actual is not None:
                actual["lineas"].append(linea)

    for f in fragmentos:
        f["texto"] = "\n".join(f["lineas"]).strip()
        del f["lineas"]
        f["tokens"] = tokenizar(f["titulo"] + " " + f["texto"])
        f["lista_titulo"] = tokenizar(f["titulo"])
        f["tokens_titulo"] = set(f["lista_titulo"])
    return fragmentos, avisos


def construir_indice(fragmentos):
    """Frecuencia documental de cada termino y longitud media de las secciones."""
    total = len(fragmentos)
    df = {}
    for f in fragmentos:
        for t in set(f["tokens"]):
            df[t] = df.get(t, 0) + 1
    longitudes = [len(f["tokens"]) for f in fragmentos] or [1]
    return {"total": total, "df": df, "longitud_media": sum(longitudes) / len(longitudes)}


def buscar(consulta, fragmentos, indice):
    """Puntua cada seccion frente a la pregunta y devuelve las mejores.

    Un termino que aparece en casi todas las secciones (por ejemplo
    'interemprex') apenas puntua. Se exige ademas una coincidencia minima para
    no devolver secciones que solo comparten una palabra omnipresente.
    """
    consulta_tokens = tokenizar(consulta)
    if not consulta_tokens:
        return [], consulta_tokens

    total, df = indice["total"], indice["df"]
    media = indice["longitud_media"]
    ubicuo = total / 2.0
    resultados = []

    for f in fragmentos:
        presentes = [t for t in set(consulta_tokens) if t in f["tokens"]]
        if not presentes:
            continue
        # Filtro: o bien coincide algo poco comun, o bien coinciden dos terminos.
        discriminantes = [t for t in presentes if df.get(t, 0) <= ubicuo]
        if not discriminantes and len(presentes) < 2:
            continue

        puntos = 0.0
        longitud = len(f["tokens"]) or 1
        for t in presentes:
            # Repetir un termino suma, pero cada repeticion suma menos que la
            # anterior (saturacion): una seccion no gana por insistir.
            tf = f["tokens"].count(t)
            tf += f["lista_titulo"].count(t) * (PESO_TITULO - 1)
            idf = log(1 + (total - df.get(t, 1) + 0.5) / (df.get(t, 1) + 0.5))
            saturado = (tf * (K1 + 1)) / (tf + K1 * (1 - B + B * longitud / media))
            puntos += idf * saturado

        resultados.append({"fragmento": f, "puntos": puntos, "coincidencias": sorted(presentes)})

    resultados.sort(key=lambda r: r["puntos"], reverse=True)
    return resultados, consulta_tokens


def avisos_de_contenido(fragmento):
    encontrados = []
    for patron, aviso in MARCAS:
        if re.search(patron, fragmento["texto"], re.M) and aviso not in encontrados:
            encontrados.append(aviso)
    return encontrados


def formatear(resultado, posicion):
    f = resultado["fragmento"]
    lineas = []
    lineas.append("-" * 78)
    lineas.append("[{}] {} · versión {} · sección {} · «{}»".format(
        posicion, f["id"], f["version"], f["seccion"], f["titulo"]))
    lineas.append("    Documento: {} ({})".format(f["titulo_documento"], f["archivo"]))
    lineas.append("    ESTADO DEL DOCUMENTO: {}".format(f["estado"]))
    avisos = avisos_de_contenido(f)
    if avisos:
        lineas.append("    AVISOS SOBRE ESTA SECCIÓN: " + "; ".join(avisos))
    lineas.append("    Coincide en: {} (puntuación {:.2f})".format(
        ", ".join(resultado["coincidencias"]), resultado["puntos"]))
    lineas.append("")
    lineas.append("    TEXTO LITERAL DE LA SECCIÓN, sin resumir ni reformular:")
    lineas.append("    " + "." * 70)
    for linea in f["texto"].splitlines():
        lineas.append("    " + linea)
    lineas.append("    " + "." * 70)
    return "\n".join(lineas)


def mensaje_sin_resultados(consulta_tokens, fragmentos):
    if not consulta_tokens:
        cabeza = ("La pregunta no contiene palabras que se puedan buscar: solo términos muy comunes.")
    else:
        cabeza = ("La búsqueda no ha encontrado ninguna sección que coincida con: {}".format(
            ", ".join(consulta_tokens)))

    indice = ["    {} §{}: {}".format(f["id"], f["seccion"], f["titulo"]) for f in fragmentos]
    return (
        "{}\n"
        "\n"
        "QUÉ SIGNIFICA ESTO, Y QUÉ NO:\n"
        "  - Significa que ESTA BÚSQUEDA no ha casado la pregunta con ninguna sección.\n"
        "    NO demuestra que las palabras falten en los documentos: antes de buscar se\n"
        "    descartan las palabras muy comunes, se recortan los plurales de forma\n"
        "    rudimentaria y se exige una coincidencia mínima. Cualquiera de esos filtros\n"
        "    puede dejar fuera un término que sí está escrito.\n"
        "  - NO significa que INTEREMPREX no ofrezca eso, ni que lo descarte. Son tres\n"
        "    borradores iniciales y hay muchísimos asuntos que todavía no se han escrito.\n"
        "  - La búsqueda compara palabras, no significados: si el documento nombra lo\n"
        "    mismo de otra forma, no lo encontrará. Por ejemplo «¿a qué se dedica?» no\n"
        "    encuentra nada, porque los documentos no usan el verbo «dedicarse».\n"
        "\n"
        "Para salir de dudas, abre los archivos de data/documentos/ y búscalo a mano.\n"
        "\n"
        "SECCIONES DISPONIBLES, por si prefieres ir directo a una:\n"
        "{}"
    ).format(cabeza, "\n".join(indice))


def main():
    fragmentos, avisos = cargar()
    for aviso in avisos:
        print("AVISO: {}".format(aviso), file=sys.stderr)
    if not fragmentos:
        print("No hay documentos que consultar en {}".format(CARPETA_DOCS), file=sys.stderr)
        return 1

    indice = construir_indice(fragmentos)
    documentos = sorted({f["archivo"] for f in fragmentos})

    print("Consulta documental de INTEREMPREX")
    print("{} secciones indexadas de {} documentos:".format(len(fragmentos), len(documentos)))
    for nombre in documentos:
        uno = next(f for f in fragmentos if f["archivo"] == nombre)
        cuantas = sum(1 for f in fragmentos if f["archivo"] == nombre)
        print("  - {} v{}: {} secciones ({})".format(uno["id"], uno["version"], cuantas, nombre))
    print()
    print("Esto es un buscador, no un asistente: muestra el texto tal cual está escrito,")
    print("sin resumirlo ni interpretarlo. Escribe /salir para terminar.")

    registro = ["# Registro de consultas — {:%Y-%m-%d %H:%M}".format(datetime.now()),
                "", "Equipo F (DESKTOP-T6C436J). Búsqueda literal, sin modelo de lenguaje.", ""]
    hubo_consultas = False

    while True:
        try:
            consulta = input("\nPregunta: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nFin de la consulta.")
            break
        if not consulta:
            continue
        if consulta.lower() in SALIDAS:
            print("Fin de la consulta.")
            break

        hubo_consultas = True
        resultados, tokens = buscar(consulta, fragmentos, indice)
        registro.append("## Pregunta: {}".format(consulta))
        registro.append("Términos buscados: {}".format(", ".join(tokens) if tokens else "(ninguno)"))
        registro.append("")

        if not resultados:
            texto = mensaje_sin_resultados(tokens, fragmentos)
            print("\n" + texto)
            registro.append("SIN RESULTADOS.")
            registro.append("")
            continue

        mostrados = resultados[:RESULTADOS]
        print("\n{} sección(es) encontradas, se muestran las {} mejores:".format(
            len(resultados), len(mostrados)))

        # Decir que parte de la pregunta no existe en los documentos evita que
        # alguien tome por respuesta una seccion que solo comparte una palabra.
        ausentes = [t for t in dict.fromkeys(tokens) if t not in indice["df"]]
        if ausentes:
            print("OJO: la búsqueda no ha casado estos términos con ninguna sección: {}.".format(
                ", ".join(ausentes)))
            print("     Lo que sigue coincide solo en el resto, así que puede no responderte.")
            print("     No demuestra que falten en los documentos: el recorte de plurales y la")
            print("     normalización pueden dejar fuera una palabra que sí está escrita.")
            registro.append("Términos no casados por la búsqueda: {}".format(", ".join(ausentes)))
        if mostrados[0]["puntos"] < UMBRAL_DEBIL:
            print("AVISO: la coincidencia es débil. Puede que ninguna sección responda de verdad.")
            registro.append("AVISO: coincidencia débil.")
        for i, r in enumerate(mostrados, 1):
            bloque = formatear(r, i)
            print("\n" + bloque)
            registro.append(bloque)
            registro.append("")
        print("-" * 78)
        print("Los textos anteriores son literales. Comprueba el estado y los avisos de")
        print("cada sección antes de tratarlos como condiciones acordadas.")
        print("La puntuación mide parecido de palabras, no que la sección responda a tu")
        print("pregunta: una puntuación alta puede acompañar a un fragmento que no sirve.")

    if hubo_consultas:
        CARPETA_REGISTRO.mkdir(parents=True, exist_ok=True)
        destino = CARPETA_REGISTRO / "consultas_{:%Y-%m-%d_%H%M%S}.md".format(datetime.now())
        destino.write_text("\n".join(registro), encoding="utf-8")
        print("\nRegistro de esta sesión guardado en: {}".format(destino))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
