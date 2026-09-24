from functools import wraps
import logging
logger = logging.getLogger(__name__)


def log_llamada(funcion):
    """crea una envoltura que nos muestra a que funcion llamamos y nos muestra la segunda clave con sus kwargs"""
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        logger.info(f"Llamando a {funcion.__name__} con args={args[1:]}, kwargs={kwargs}")
        resultado = funcion(*args, **kwargs)
        return resultado
    return envoltura