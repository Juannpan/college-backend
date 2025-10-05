from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import participacion as participacion_crud
from app.models.participacion import ParticipacionModel
from app.schemas.participacion import ParticipacionCrear, ParticipacionActualizar


async def crear_participacion_service(session: AsyncSession, nueva_participacion: ParticipacionCrear) -> ParticipacionModel:
    try:
        return await participacion_crud.crear_participacion(session, nueva_participacion)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al crear la participación (posiblemente ya exista un registro similar)."
        ) from e


async def listar_participaciones_service(session: AsyncSession) -> Sequence[ParticipacionModel]:
    return await participacion_crud.listar_participaciones(session)


async def buscar_participacion_por_id_service(session: AsyncSession, participacion_id: int) -> ParticipacionModel:
    participacion = await participacion_crud.buscar_participacion_por_id(session, participacion_id)
    if not participacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe participación con id {participacion_id}"
        )
    return participacion


async def eliminar_participacion_por_id_service(session: AsyncSession, participacion_id: int) -> None:
    participacion = await participacion_crud.buscar_participacion_por_id(session, participacion_id)
    if not participacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe participación con id {participacion_id}"
        )
    eliminado = await participacion_crud.eliminar_participacion_por_id(session, participacion_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la participación"
        )
    await session.commit()


async def editar_participacion_por_id_service(session: AsyncSession, participacion_id: int, participacion_actualizar: ParticipacionActualizar):
    participacion = await participacion_crud.buscar_participacion_por_id(session, participacion_id)
    if not participacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe participación con id {participacion_id}"
        )
    actualizado = await participacion_crud.editar_participacion_por_id(session, participacion_id, participacion_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la participación"
        )
    await session.commit()
    return await participacion_crud.buscar_participacion_por_id(session, participacion_id)
