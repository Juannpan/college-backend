from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.instalacion import InstalacionModel
from app.schemas.instalacion import InstalacionCrear, InstalacionActualizar

async def crear_instalacion(session: AsyncSession, instalacion_in: InstalacionCrear) -> InstalacionModel:
    obj = InstalacionModel(**instalacion_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_instalaciones(session: AsyncSession) -> Sequence[InstalacionModel]:
    stmt = select(InstalacionModel).order_by(InstalacionModel.idInstalacion)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_instalacion_por_id(session: AsyncSession, instalacion_id: int) -> Optional[InstalacionModel]:
    stmt = select(InstalacionModel).where(InstalacionModel.idInstalacion == instalacion_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_instalacion_por_id(session: AsyncSession, instalacion_id: int) -> bool:
    stmt = delete(InstalacionModel).where(InstalacionModel.idInstalacion == instalacion_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_instalacion_por_id(
    session: AsyncSession,
    instalacion_id: int,
    instalacion_actualizar: InstalacionActualizar
) -> bool:
    values = instalacion_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(InstalacionModel)
        .where(InstalacionModel.idInstalacion == instalacion_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
