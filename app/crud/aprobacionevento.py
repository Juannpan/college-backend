from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.aprobacionevento import AprobacionEventoModel
from app.schemas.aprobacionevento import AprobacionEventoCrear, AprobacionEventoActualizar

async def crear_aprobacionevento(session: AsyncSession, aprobacion_in: AprobacionEventoCrear) -> AprobacionEventoModel:
    obj = AprobacionEventoModel(**aprobacion_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_aprobacioneventos(session: AsyncSession) -> Sequence[AprobacionEventoModel]:
    stmt = select(AprobacionEventoModel).order_by(AprobacionEventoModel.idAprobacion)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_aprobacionevento_por_id(session: AsyncSession, aprobacion_id: int) -> Optional[AprobacionEventoModel]:
    stmt = (
        select(AprobacionEventoModel)
        .options(selectinload(AprobacionEventoModel.evento), selectinload(AprobacionEventoModel.secretaria))
        .where(AprobacionEventoModel.idAprobacion == aprobacion_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_aprobacionevento_por_id(session: AsyncSession, aprobacion_id: int) -> bool:
    stmt = delete(AprobacionEventoModel).where(AprobacionEventoModel.idAprobacion == aprobacion_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_aprobacionevento_por_id(
    session: AsyncSession,
    aprobacion_id: int,
    aprobacion_actualizar: AprobacionEventoActualizar
) -> bool:
    values = aprobacion_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(AprobacionEventoModel)
        .where(AprobacionEventoModel.idAprobacion == aprobacion_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
