from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.organizacionparticipacion import OrganizacionParticipacionModel
from app.schemas.organizacionparticipacion import (
    OrganizacionParticipacionCrear,
    OrganizacionParticipacionActualizar,
)


async def crear_organizacionparticipacion(
    session: AsyncSession, org_part_in: OrganizacionParticipacionCrear
) -> OrganizacionParticipacionModel:
    obj = OrganizacionParticipacionModel(**org_part_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def listar_organizacionparticipaciones(session: AsyncSession) -> Sequence[OrganizacionParticipacionModel]:
    stmt = select(OrganizacionParticipacionModel).order_by(
        OrganizacionParticipacionModel.idParticipacionExterna
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def buscar_organizacionparticipacion_por_id(
    session: AsyncSession, org_part_id: int
) -> Optional[OrganizacionParticipacionModel]:
    stmt = select(OrganizacionParticipacionModel).where(
        OrganizacionParticipacionModel.idParticipacionExterna == org_part_id
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def eliminar_organizacionparticipacion_por_id(session: AsyncSession, org_part_id: int) -> bool:
    stmt = delete(OrganizacionParticipacionModel).where(
        OrganizacionParticipacionModel.idParticipacionExterna == org_part_id
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def editar_organizacionparticipacion_por_id(
    session: AsyncSession, org_part_id: int, org_part_actualizar: OrganizacionParticipacionActualizar
) -> bool:
    values = org_part_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(OrganizacionParticipacionModel)
        .where(OrganizacionParticipacionModel.idParticipacionExterna == org_part_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
