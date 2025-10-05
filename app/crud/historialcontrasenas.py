from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.historialcontrasenas import HistorialContrasenasModel
from app.schemas.historialcontrasenas import HistorialContrasenasCrear, HistorialContrasenasActualizar

async def crear_historial_contrasena(session: AsyncSession, historial_in: HistorialContrasenasCrear) -> HistorialContrasenasModel:
    obj = HistorialContrasenasModel(**historial_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_historial_contrasenas(session: AsyncSession) -> Sequence[HistorialContrasenasModel]:
    stmt = select(HistorialContrasenasModel).order_by(HistorialContrasenasModel.idHistorial)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_historial_por_id(session: AsyncSession, historial_id: int) -> Optional[HistorialContrasenasModel]:
    stmt = select(HistorialContrasenasModel).where(HistorialContrasenasModel.idHistorial == historial_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_historial_por_id(session: AsyncSession, historial_id: int) -> bool:
    stmt = delete(HistorialContrasenasModel).where(HistorialContrasenasModel.idHistorial == historial_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_historial_por_id(
    session: AsyncSession,
    historial_id: int,
    historial_actualizar: HistorialContrasenasActualizar
) -> bool:
    values = historial_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(HistorialContrasenasModel)
        .where(HistorialContrasenasModel.idHistorial == historial_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
