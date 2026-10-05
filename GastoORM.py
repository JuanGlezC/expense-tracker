from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class GastoORM(Base):
    __tablename__ = "gastos"

    id: Mapped[str] = mapped_column(primary_key=True)
    categoria: Mapped[str]
    importe: Mapped[float]
    fecha: Mapped[str]
    descripcion: Mapped[str | None]