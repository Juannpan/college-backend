from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.estudiante import EstudianteModel
from app.schemas.estudiante import EstudianteCrear, EstudianteActualizar

async def crear_estudiante(session: AsyncSession, estudiante_in: EstudianteCrear) -> EstudianteModel:
    obj = EstudianteModel(**estudiante_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_estudiantes(session: AsyncSession) -> Sequence[EstudianteModel]:
    stmt = select(EstudianteModel).order_by(EstudianteModel.idPersona)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_estudiante_por_id(session: AsyncSession, estudiante_id: int) -> Optional[EstudianteModel]:
    stmt = (
        select(EstudianteModel)
        .options(selectinload(EstudianteModel.persona), selectinload(EstudianteModel.programa))
        .where(EstudianteModel.idPersona == estudiante_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_estudiante_por_id(session: AsyncSession, estudiante_id: int) -> bool:
    stmt = delete(EstudianteModel).where(EstudianteModel.idPersona == estudiante_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_estudiante_por_id(
    session: AsyncSession,
    estudiante_id: int,
    estudiante_actualizar: EstudianteActualizar
) -> bool:
    values = estudiante_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(EstudianteModel)
        .where(EstudianteModel.idPersona == estudiante_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
