import requests
from .models import Atleta

numAtletas = 4
HOST = "127.0.0.1"
PORT = 8080
FICHERO = "resultados.log"


def start():
    reinicio = requests.get(f"http://{HOST}:{PORT}/reinicio")

    atletas = []
    for num in range(numAtletas):
        atletas.append(Atleta(dorsal="10" + str(num)))

    for atleta in atletas:
        atleta.start()
    print("Atletas -> Hilos START")

    for atleta in atletas:
        atleta.join()

    with open(FICHERO, "a+") as f:
        resultados = requests.get(f"http://{HOST}:{PORT}/resultados")
        print(resultados.text)
        f.write(resultados.text)
