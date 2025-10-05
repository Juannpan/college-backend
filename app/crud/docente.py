from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.docente import DocenteModel
from app.schemas.docente import DocenteCrear, DocenteActualizar

async def crear_docente(session: AsyncSession, docente_in: DocenteCrear) -> DocenteModel:
    obj = DocenteModel(**docente_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_docentes(session: AsyncSession) -> Sequence[DocenteModel]:
    stmt = select(DocenteModel).order_by(DocenteModel.idPersona)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_docente_por_id(session: AsyncSession, docente_id: int) -> Optional[DocenteModel]:
    stmt = (
        select(DocenteModel)
        .options(selectinload(DocenteModel.persona), selectinload(DocenteModel.unidad))
        .where(DocenteModel.idPersona == docente_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_docente_por_id(session: AsyncSession, docente_id: int) -> bool:
    stmt = delete(DocenteModel).where(DocenteModel.idPersona == docente_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_docente_por_id(
    session: AsyncSession,
    docente_id: int,
    docente_actualizar: DocenteActualizar
) -> bool:
    values = docente_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(DocenteModel)
        .where(DocenteModel.idPersona == docente_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
