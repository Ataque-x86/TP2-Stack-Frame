import requests
import ctypes

# Cargamos la libreria
lib_converter = ctypes.CDLL("./to_int_plus_one.so")

# Definimos los tipos de los argumentos de la función factorial
lib_converter.to_int_plus_one.argtypes = (ctypes.c_float,)

# Definimos el tipo del retorno de la función factorial
lib_converter.to_int_plus_one.restype = ctypes.c_int


# Creamos nuestra función factorial en Python
# hace de Wrapper para llamar a la función de C
def float_to_int_plus_one(num):
    return lib_converter.to_int_plus_one(num)


flag = True

print(
    "gini>> Este es un programa para obtener los valores, de un cierto pais, del indice GINI\n"
)

while flag:
    country = input("gini>> Ingrese un pais: ")

    URL = f"https://api.worldbank.org/v2/country/{country}/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=1000"

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        print("gini>> No se pudo consultar la API del Banco Mundial.\n")
        flag = input("Continuar --> 1\nFinalizar --> 0\n").strip() == "1"
        continue
    except ValueError:
        print("gini>> La API devolvio una respuesta invalida.\n")
        flag = input("Continuar --> 1\nFinalizar --> 0\n").strip() == "1"
        continue

    if len(data) < 2 or not isinstance(data[1], list):
        print("gini>> No se encontraron datos para el pais ingresado.\n")
        flag = input("Continuar --> 1\nFinalizar --> 0\n").strip() == "1"
        continue

    values = data[1]
    found_values = False

    for item in values:
        if item["value"] is None:
            continue
        found_values = True
        print(f"date: {item['date']}, value: {item['value']}\n")
        int_converted = float_to_int_plus_one(item["value"])
        print(f"date: {item['date']}, value: {int_converted}\n")

    if not found_values:
        print("gini>> El pais ingresado no tiene valores GINI disponibles en ese rango.\n")

    flag = input("Continuar --> 1\nFinalizar --> 0\n").strip() == "1"


print("Programa finalizado.")
