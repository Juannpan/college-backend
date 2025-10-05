from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import organizacion as organizacion_crud
from app.models.organizacion import OrganizacionModel
from app.schemas.organizacion import OrganizacionCrear, OrganizacionActualizar


async def crear_organizacion_service(session: AsyncSession, nueva_organizacion: OrganizacionCrear) -> OrganizacionModel:
    try:
        return await organizacion_crud.crear_organizacion(session, nueva_organizacion)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una organización con ese nombre o ID."
        ) from e


async def listar_organizaciones_service(session: AsyncSession) -> Sequence[OrganizacionModel]:
    return await organizacion_crud.listar_organizaciones(session)


async def buscar_organizacion_por_id_service(session: AsyncSession, organizacion_id: int) -> OrganizacionModel:
    organizacion = await organizacion_crud.buscar_organizacion_por_id(session, organizacion_id)
    if not organizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe organización con id {organizacion_id}"
        )
    return organizacion


async def eliminar_organizacion_por_id_service(session: AsyncSession, organizacion_id: int) -> None:
    organizacion = await organizacion_crud.buscar_organizacion_por_id(session, organizacion_id)
    if not organizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe organización con id {organizacion_id}"
        )
    eliminado = await organizacion_crud.eliminar_organizacion_por_id(session, organizacion_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la organización"
        )
    await session.commit()


async def editar_organizacion_por_id_service(session: AsyncSession, organizacion_id: int, organizacion_actualizar: OrganizacionActualizar):
    organizacion = await organizacion_crud.buscar_organizacion_por_id(session, organizacion_id)
    if not organizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe organización con id {organizacion_id}"
        )
    actualizado = await organizacion_crud.editar_organizacion_por_id(session, organizacion_id, organizacion_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la organización"
        )
    await session.commit()
    return await organizacion_crud.buscar_organizacion_por_id(session, organizacion_id)
