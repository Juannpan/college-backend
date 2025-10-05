from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.organizacion import OrganizacionModel
from app.schemas.organizacion import OrganizacionCrear, OrganizacionActualizar

async def crear_organizacion(session: AsyncSession, organizacion_in: OrganizacionCrear) -> OrganizacionModel:
    obj = OrganizacionModel(**organizacion_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_organizaciones(session: AsyncSession) -> Sequence[OrganizacionModel]:
    stmt = select(OrganizacionModel).order_by(OrganizacionModel.idOrganizacion)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_organizacion_por_id(session: AsyncSession, organizacion_id: int) -> Optional[OrganizacionModel]:
    stmt = select(OrganizacionModel).where(OrganizacionModel.idOrganizacion == organizacion_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_organizacion_por_id(session: AsyncSession, organizacion_id: int) -> bool:
    stmt = delete(OrganizacionModel).where(OrganizacionModel.idOrganizacion == organizacion_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_organizacion_por_id(
    session: AsyncSession,
    organizacion_id: int,
    organizacion_actualizar: OrganizacionActualizar
) -> bool:
    values = organizacion_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(OrganizacionModel)
        .where(OrganizacionModel.idOrganizacion == organizacion_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
