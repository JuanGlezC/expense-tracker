from sqlalchemy import select
from sqlalchemy.orm import Session
from GastoORM import GastoORM
from gasto import Gasto

def agregar_gasto(engine, gasto: Gasto) -> None:
    """convierte el Gasto de dominio a GastoORM y lo persiste inmediatamente en la base de datos"""
    gasto_orm = GastoORM(
        id=gasto.id,
        categoria=gasto.categoria,
        importe=gasto.importe,
        fecha=gasto.fecha,
    )
    with Session(engine) as sesion:
        sesion.add(gasto_orm)
        sesion.commit()


def cargar_gastos(engine) -> list[Gasto]:
    """consulta todos los GastoORM de la tabla y los convierte de vuelta a Gasto de dominio"""
    with Session(engine) as sesion:
        gastos_orm = sesion.scalars(select(GastoORM)).all()
        return [
            Gasto(id=g.id, categoria=g.categoria, importe=g.importe, fecha=g.fecha)
            for g in gastos_orm
        ]
