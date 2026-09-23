from functools import wraps
import logging
logger = logging.getLogger(__name__)


def log_llamada(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        logger.info(f"Llamando a {funcion.__name__} con args={args[1:]}, kwargs={kwargs}")
        resultado = funcion(*args, **kwargs)
        return resultado
    return envoltura