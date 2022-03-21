import uvicorn
import logging
import time
from fastapi import FastAPI
from .models import Atleta, Shot, Variables

numAtletas = 4
HOST = "127.0.0.1"
PORT = 8080
FICHERO = "resultados.log"

tiempoIni = 0
tiempoFin = 0
atletas = {}
pistoletazo = Shot()
finCarrera = Shot()
variables = Variables()

logger = logging.getLogger(__name__)
api = FastAPI()


@api.get("/reinicio")
async def reinicio():
    variables.reiniciar()
    tiempoIni = 0
    atletas = {}
    message = "Variables reiniciadas."
    return {"message": message}


@api.get("/preparado")
async def preparado():
    print("Preparado")
    numPreparados = variables.actualizar("preparados")
    print("NumPreparados:", numPreparados)
    if numPreparados < numAtletas:
        print("Me espero mi pana")
        pistoletazo.wait()
    else:
        print("ARRANCAMIOS LEEROY JENKINS")
        pistoletazo.notify()
    message = "Preparados..."
    return {"message": message}


@api.get("/listo")
async def listo():
    numListos = variables.actualizar("listos")
    if numListos < numAtletas:
        pistoletazo.wait()
    else:
        pistoletazo.notify()
        tiempoIni = time.time()
    message = "Listo..."
    return {"message": message}


@api.get("/llegada")
async def llegada(dorsal: int):
    tiempoFin = time.time() - tiempoIni
    atletas[dorsal] = tiempoFin
    numFinalizados: int = variables.actualizar("finalizados")
    if numFinalizados == numAtletas:
        finCarrera.notify()
    message = f"{tiempoFin}"
    return {"message": message}


@api.get("/resultados")
async def resultados():
    finCarrera.wait()
    message = ""
    for key, value in atletas.items():
        message = message + f"Atleta {key}: {value} segundos.\n"
    return {"message": message}


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("main.main:api", host=HOST, port=PORT)
