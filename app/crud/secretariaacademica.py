from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.secretariaacademica import SecretariaAcademicaModel
from app.schemas.secretariaacademica import SecretariaAcademicaCrear, SecretariaAcademicaActualizar

async def crear_secretaria_academica(session: AsyncSession, secretaria_in: SecretariaAcademicaCrear) -> SecretariaAcademicaModel:
    obj = SecretariaAcademicaModel(**secretaria_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_secretarias_academicas(session: AsyncSession) -> Sequence[SecretariaAcademicaModel]:
    stmt = select(SecretariaAcademicaModel).order_by(SecretariaAcademicaModel.idSecretariaAcademica)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_secretaria_academica_por_id(session: AsyncSession, secretaria_id: int) -> Optional[SecretariaAcademicaModel]:
    stmt = select(SecretariaAcademicaModel).where(SecretariaAcademicaModel.idSecretariaAcademica == secretaria_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_secretaria_academica_por_id(session: AsyncSession, secretaria_id: int) -> bool:
    stmt = delete(SecretariaAcademicaModel).where(SecretariaAcademicaModel.idSecretariaAcademica == secretaria_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_secretaria_academica_por_id(
    session: AsyncSession,
    secretaria_id: int,
    secretaria_actualizar: SecretariaAcademicaActualizar
) -> bool:
    values = secretaria_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(SecretariaAcademicaModel)
        .where(SecretariaAcademicaModel.idSecretariaAcademica == secretaria_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
