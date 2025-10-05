from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.unidad import UnidadModel
from app.schemas.unidad import UnidadCrear, UnidadActualizar

async def crear_unidad(session: AsyncSession, unidad_in: UnidadCrear) -> UnidadModel:
    obj = UnidadModel(**unidad_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_unidades(session: AsyncSession) -> Sequence[UnidadModel]:
    stmt = select(UnidadModel).order_by(UnidadModel.idUnidad)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_unidad_por_id(session: AsyncSession, unidad_id: int) -> Optional[UnidadModel]:
    stmt = select(UnidadModel).where(UnidadModel.idUnidad == unidad_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_unidad_por_id(session: AsyncSession, unidad_id: int) -> bool:
    stmt = delete(UnidadModel).where(UnidadModel.idUnidad == unidad_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_unidad_por_id(
    session: AsyncSession,
    unidad_id: int,
    unidad_actualizar: UnidadActualizar
) -> bool:
    values = unidad_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(UnidadModel)
        .where(UnidadModel.idUnidad == unidad_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
