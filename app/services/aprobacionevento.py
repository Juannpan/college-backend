from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import aprobacionevento as aprobacionevento_crud
from app.models.aprobacionevento import AprobacionEventoModel
from app.schemas.aprobacionevento import AprobacionEventoCrear, AprobacionEventoActualizar


async def crear_aprobacionevento_service(session: AsyncSession, nueva_aprobacion: AprobacionEventoCrear) -> AprobacionEventoModel:
    try:
        aprobacion_creada = await aprobacionevento_crud.crear_aprobacionevento(session, nueva_aprobacion)
        return aprobacion_creada
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una aprobación con ese ID."
        ) from e


async def listar_aprobacioneseventos_service(session: AsyncSession) -> Sequence[AprobacionEventoModel]:
    return await aprobacionevento_crud.listar_aprobacioneseventos(session)


async def buscar_aprobacionevento_por_id_service(session: AsyncSession, aprobacion_id: int) -> AprobacionEventoModel:
    aprobacion = await aprobacionevento_crud.buscar_aprobacionevento_por_id(session, aprobacion_id)
    if not aprobacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe aprobación con id {aprobacion_id}"
        )
    return aprobacion


async def eliminar_aprobacionevento_por_id_service(session: AsyncSession, aprobacion_id: int) -> None:
    aprobacion = await aprobacionevento_crud.buscar_aprobacionevento_por_id(session, aprobacion_id)
    if not aprobacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe aprobación con id {aprobacion_id}"
        )
    eliminado = await aprobacionevento_crud.eliminar_aprobacionevento_por_id(session, aprobacion_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la aprobación"
        )
    await session.commit()


async def editar_aprobacionevento_por_id_service(session: AsyncSession, aprobacion_id: int, aprobacion_actualizar: AprobacionEventoActualizar):
    aprobacion = await aprobacionevento_crud.buscar_aprobacionevento_por_id(session, aprobacion_id)
    if not aprobacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe aprobación con id {aprobacion_id}"
        )
    actualizado = await aprobacionevento_crud.editar_aprobacionevento_por_id(session, aprobacion_id, aprobacion_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la aprobación"
        )
    await session.commit()
    return await aprobacionevento_crud.buscar_aprobacionevento_por_id(session, aprobacion_id)
