import platform
import sys

print("Equipo:", platform.node())
print("Python:", sys.executable)
print("Entorno virtual:", sys.prefix != sys.base_prefix)
