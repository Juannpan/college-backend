from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.director import DirectorModel
from app.schemas.director import DirectorCrear, DirectorActualizar

async def crear_director(session: AsyncSession, director_in: DirectorCrear) -> DirectorModel:
    obj = DirectorModel(**director_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_directores(session: AsyncSession) -> Sequence[DirectorModel]:
    stmt = select(DirectorModel).order_by(DirectorModel.idPersona)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_director_por_id(session: AsyncSession, director_id: int) -> Optional[DirectorModel]:
    stmt = (
        select(DirectorModel)
        .options(selectinload(DirectorModel.persona))
        .where(DirectorModel.idPersona == director_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_director_por_id(session: AsyncSession, director_id: int) -> bool:
    stmt = delete(DirectorModel).where(DirectorModel.idPersona == director_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_director_por_id(
    session: AsyncSession,
    director_id: int,
    director_actualizar: DirectorActualizar
) -> bool:
    values = director_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(DirectorModel)
        .where(DirectorModel.idPersona == director_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
