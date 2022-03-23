from threading import Thread, Condition, Lock
from time import sleep
import requests
from random import uniform as rango_float
from threading import Lock

numAtletas = 4
HOST = "127.0.0.1"
PORT = 8080
FICHERO = "resultados.log"


# https://www.caffeinatedideas.com/2014/12/12/java-synchronized-in-python.html
def synchronized(method):
    """
    A decorator object that can be used to declare that execution of a particular
    method should be done synchronous. This works by maintaining a lock object on
    the object instance, constructed for you if you don't have one already, and
    then acquires the lock before allowing the method to execute. This provides
    similar semantics to Java's synchronized keyword on methods.
    """

    def new_synchronized_method(self, *args, **kwargs):
        if not hasattr(self, "_auto_lock"):
            self._auto_lock = Lock()
        with self._auto_lock:
            return method(self, *args, **kwargs)

    return new_synchronized_method


class Shot:
    """Clase manejadora de los hilos. Define las funciones para la gestión de la concurrencia y notificación a los demás hilos."""

    def __init__(self):
        """ """
        self._cond = Condition(Lock())
        self._flag = False

    def is_set(self):
        """Devuelve el valor de la flag.
        Returns:
            flag (bool): Condición de espera.
        """
        return self._flag

    # @synchronized
    def wait(self, timeout=None):
        """Si el flag es falso, espera a que sea notificado.
        Args:
            timeout (int, optional): Tiempo a esperar máximo. Por defecto es: None.
        Returns:
            flag (bool): Se devuelve si es verdadero (no está esperando).
        """
        self._cond.acquire()
        try:
            signaled = self._flag
            if not signaled:
                signaled = self._cond.wait(timeout)
            return signaled
        finally:
            pass
            self._cond.release()

    # @synchronized
    def notify(self):
        """Habilita la flag a verdadero y lo notifica. Dejando así los hilos que estuvieran bloqueados ejecutar sus funciones."""
        self._cond.acquire()
        try:
            self._flag = True
            self._cond.notify_all()
        finally:
            pass
            self._cond.release()


class Atleta(Thread):
    """Clase del atleta, hereda de la clase Thread."""

    def __init__(
        self,
        dorsal: str,
    ):
        self.dorsal = dorsal
        Thread.__init__(self)

    def start_race(self):
        with open(FICHERO, "a+") as f:

            preparado = requests.get(f"http://{HOST}:{PORT}/preparado")
            print(preparado.text)
            f.write(f"{self.dorsal}: {preparado.text}\n")

            listo = requests.get(f"http://{HOST}:{PORT}/listo")
            print(listo.text)
            f.write(f"{self.dorsal}: {listo.text}\n")

            """Espera un tiempo entre 9.56 y 11.76 segundos y lo imprime por pantalla."""
            sleep(rango_float(9.56, 11.76))

            llegada = requests.get(f"http://{HOST}:{PORT}/llegada/{self.dorsal}")
            print(llegada.text)
            f.write(f"{self.dorsal}: {llegada.text}\n")

    def run(self):
        """Método que sobrescribe al propio de la clase Thread.
        Realiza el bloqueo hasta recibir la notificación, entonces ejecuta ciertas funciones.
        """
        self.start_race()


class Variables:
    def __init__(
        self, numPreparados: int = 0, numListos: int = 0, numFinalizados: int = 0
    ):
        self.numPreparados = numPreparados
        self.numListos = numListos
        self.numFinalizados = numFinalizados

    # @synchronized
    def actualizar(self, variable: str) -> int:
        if variable == "preparados":
            self.numPreparados = self.numPreparados + 1
            return self.numPreparados
        elif variable == "listos":
            self.numListos = self.numListos + 1
            return self.numListos
        else:
            self.numFinalizados = self.numListos + 1
            return self.numFinalizados

    # @synchronized
    def reiniciar(self) -> None:
        self.numPreparados = 0
        self.numListos = 0
        self.numFinalizados = 0
