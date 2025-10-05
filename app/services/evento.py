from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import evento as evento_crud
from app.models.evento import EventoModel
from app.schemas.evento import EventoCrear, EventoActualizar


async def crear_evento_service(session: AsyncSession, nuevo_evento: EventoCrear) -> EventoModel:
    try:
        return await evento_crud.crear_evento(session, nuevo_evento)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un evento con ese ID."
        ) from e


async def listar_eventos_service(session: AsyncSession) -> Sequence[EventoModel]:
    return await evento_crud.listar_eventos(session)


async def buscar_evento_por_id_service(session: AsyncSession, evento_id: int) -> EventoModel:
    evento = await evento_crud.buscar_evento_por_id(session, evento_id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe evento con id {evento_id}"
        )
    return evento


async def eliminar_evento_por_id_service(session: AsyncSession, evento_id: int) -> None:
    evento = await evento_crud.buscar_evento_por_id(session, evento_id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe evento con id {evento_id}"
        )
    eliminado = await evento_crud.eliminar_evento_por_id(session, evento_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el evento"
        )
    await session.commit()


async def editar_evento_por_id_service(session: AsyncSession, evento_id: int, evento_actualizar: EventoActualizar):
    evento = await evento_crud.buscar_evento_por_id(session, evento_id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe evento con id {evento_id}"
        )
    actualizado = await evento_crud.editar_evento_por_id(session, evento_id, evento_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar el evento"
        )
    await session.commit()
    return await evento_crud.buscar_evento_por_id(session, evento_id)
