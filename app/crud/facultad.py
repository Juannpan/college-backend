from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.facultad import FacultadModel
from app.schemas.facultad import FacultadCrear, FacultadActualizar

async def crear_facultad(session: AsyncSession, facultad_in: FacultadCrear) -> FacultadModel:
    obj = FacultadModel(**facultad_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_facultades(session: AsyncSession) -> Sequence[FacultadModel]:
    stmt = select(FacultadModel).order_by(FacultadModel.idFacultad)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_facultad_por_id(session: AsyncSession, facultad_id: int) -> Optional[FacultadModel]:
    stmt = select(FacultadModel).where(FacultadModel.idFacultad == facultad_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_facultad_por_id(session: AsyncSession, facultad_id: int) -> bool:
    stmt = delete(FacultadModel).where(FacultadModel.idFacultad == facultad_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_facultad_por_id(
    session: AsyncSession,
    facultad_id: int,
    facultad_actualizar: FacultadActualizar
) -> bool:
    values = facultad_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(FacultadModel)
        .where(FacultadModel.idFacultad == facultad_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
