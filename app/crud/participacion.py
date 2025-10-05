from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.participacion import ParticipacionModel
from app.schemas.participacion import ParticipacionCrear, ParticipacionActualizar

async def crear_participacion(session: AsyncSession, participacion_in: ParticipacionCrear) -> ParticipacionModel:
    obj = ParticipacionModel(**participacion_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_participaciones(session: AsyncSession) -> Sequence[ParticipacionModel]:
    stmt = select(ParticipacionModel).order_by(ParticipacionModel.idParticipacion)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_participacion_por_id(session: AsyncSession, participacion_id: int) -> Optional[ParticipacionModel]:
    stmt = select(ParticipacionModel).where(ParticipacionModel.idParticipacion == participacion_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_participacion_por_id(session: AsyncSession, participacion_id: int) -> bool:
    stmt = delete(ParticipacionModel).where(ParticipacionModel.idParticipacion == participacion_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_participacion_por_id(
    session: AsyncSession,
    participacion_id: int,
    participacion_actualizar: ParticipacionActualizar
) -> bool:
    values = participacion_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(ParticipacionModel)
        .where(ParticipacionModel.idParticipacion == participacion_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
