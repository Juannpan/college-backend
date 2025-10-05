from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.programa import ProgramaModel
from app.schemas.programa import ProgramaCrear, ProgramaActualizar

async def crear_programa(session: AsyncSession, programa_in: ProgramaCrear) -> ProgramaModel:
    obj = ProgramaModel(**programa_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_programas(session: AsyncSession) -> Sequence[ProgramaModel]:
    stmt = select(ProgramaModel).order_by(ProgramaModel.idPrograma)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_programa_por_id(session: AsyncSession, programa_id: int) -> Optional[ProgramaModel]:
    stmt = select(ProgramaModel).where(ProgramaModel.idPrograma == programa_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_programa_por_id(session: AsyncSession, programa_id: int) -> bool:
    stmt = delete(ProgramaModel).where(ProgramaModel.idPrograma == programa_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_programa_por_id(
    session: AsyncSession,
    programa_id: int,
    programa_actualizar: ProgramaActualizar
) -> bool:
    values = programa_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(ProgramaModel)
        .where(ProgramaModel.idPrograma == programa_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
