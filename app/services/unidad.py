from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import unidad as unidad_crud
from app.models.unidad import UnidadModel
from app.schemas.unidad import UnidadCrear, UnidadActualizar


async def crear_unidad_service(session: AsyncSession, nueva_unidad: UnidadCrear) -> UnidadModel:
    try:
        return await unidad_crud.crear_unidad(session, nueva_unidad)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una unidad con ese ID."
        ) from e


async def listar_unidades_service(session: AsyncSession) -> Sequence[UnidadModel]:
    return await unidad_crud.listar_unidades(session)


async def buscar_unidad_por_id_service(session: AsyncSession, unidad_id: int) -> UnidadModel:
    unidad = await unidad_crud.buscar_unidad_por_id(session, unidad_id)
    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe unidad con id {unidad_id}"
        )
    return unidad


async def eliminar_unidad_por_id_service(session: AsyncSession, unidad_id: int) -> None:
    unidad = await unidad_crud.buscar_unidad_por_id(session, unidad_id)
    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe unidad con id {unidad_id}"
        )
    eliminado = await unidad_crud.eliminar_unidad_por_id(session, unidad_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la unidad"
        )
    await session.commit()


async def editar_unidad_por_id_service(session: AsyncSession, unidad_id: int, unidad_actualizar: UnidadActualizar):
    unidad = await unidad_crud.buscar_unidad_por_id(session, unidad_id)
    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe unidad con id {unidad_id}"
        )
    actualizado = await unidad_crud.editar_unidad_por_id(session, unidad_id, unidad_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la unidad"
        )
    await session.commit()
    return await unidad_crud.buscar_unidad_por_id(session, unidad_id)
