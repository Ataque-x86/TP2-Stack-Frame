import requests
import ctypes
import matplotlib.pyplot as plt


#hola
# Cargamos la libreria 
lib_converter = ctypes.CDLL('./to_int_plus_one.so')

lib_converter.to_int_plus_one.argtypes = (ctypes.c_float,)
lib_converter.to_int_plus_one.restype = ctypes.c_int

def float_to_int_plus_one(num):
    return lib_converter.to_int_plus_one(num)


print("gini>> Programa para obtener valores del índice GINI\n")

flag = True

while(flag):
    country = input("gini>> Ingrese un pais (ej: AR): ")

    URL = f"https://api.worldbank.org/v2/country/{country}/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=1000"

    response = requests.get(URL)
    values = response.json()[1]

    years = []
    gini_values = []

    for item in values:
        if item["value"] is None:
            continue

        year = int(item["date"])
        value = item["value"]

        print(f"date: {item['date']}, value: {value}")

        int_converted = float_to_int_plus_one(value)

        print(f"date: {item['date']}, value (procesado): {int_converted}\n")

        # guardar para gráfico
        years.append(year)
        gini_values.append(value)

    # ordenar por año
    combined = list(zip(years, gini_values))
    combined.sort()

    years_sorted, values_sorted = zip(*combined)

    # 📊 GRAFICO
    plt.figure()
    plt.plot(years_sorted, values_sorted)
    plt.xlabel("Año")
    plt.ylabel("Índice GINI")
    plt.title(f"Índice GINI - {country.upper()}")
    plt.grid()

    plt.show()  # abre la ventana

    flag = input("Continuar --> 1\nFinalizar --> 0\n")
    if flag != "1":
        break

print("Programa finalizado.")