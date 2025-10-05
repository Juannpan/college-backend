from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.evento import EventoModel
from app.schemas.evento import EventoCrear, EventoActualizar

async def crear_evento(session: AsyncSession, evento_in: EventoCrear) -> EventoModel:
    obj = EventoModel(**evento_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_eventos(session: AsyncSession) -> Sequence[EventoModel]:
    stmt = (
        select(EventoModel)
        .options(selectinload(EventoModel.instalacion), selectinload(EventoModel.responsable))
        .order_by(EventoModel.idEvento)
    )
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_evento_por_id(session: AsyncSession, evento_id: int) -> Optional[EventoModel]:
    stmt = (
        select(EventoModel)
        .options(
            selectinload(EventoModel.instalacion),
            selectinload(EventoModel.responsable),
            selectinload(EventoModel.aprobaciones),
            selectinload(EventoModel.participaciones),
            selectinload(EventoModel.organizaciones_participantes),
        )
        .where(EventoModel.idEvento == evento_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_evento_por_id(session: AsyncSession, evento_id: int) -> bool:
    stmt = delete(EventoModel).where(EventoModel.idEvento == evento_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_evento_por_id(
    session: AsyncSession,
    evento_id: int,
    evento_actualizar: EventoActualizar
) -> bool:
    values = evento_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(EventoModel)
        .where(EventoModel.idEvento == evento_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
