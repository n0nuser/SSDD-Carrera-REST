import requests
from models import Atleta
import os

numAtletas = 4
HOST = "127.0.0.1"
PORT = 8080
FICHERO = "resultados.log"

reinicio = requests.get(f"http://{HOST}:{PORT}/reinicio")

atletas = []
for num in range(numAtletas):
    print(num)
    atletas.append(Atleta(dorsal="10" + str(num)))
    print("okay!")

print("Atletas comienzan")
for atleta in atletas:
    atleta.start()
print("Atletas han comenzado")

resultados = requests.get(f"http://{HOST}:{PORT}/resultados")
with open(FICHERO, "a+") as f:
    f.write(reinicio)
    f.write(resultados)
