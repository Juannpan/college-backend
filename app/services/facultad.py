from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import facultad as facultad_crud
from app.models.facultad import FacultadModel
from app.schemas.facultad import FacultadCrear, FacultadActualizar


async def crear_facultad_service(session: AsyncSession, nueva_facultad: FacultadCrear) -> FacultadModel:
    try:
        return await facultad_crud.crear_facultad(session, nueva_facultad)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una facultad con ese ID."
        ) from e


async def listar_facultades_service(session: AsyncSession) -> Sequence[FacultadModel]:
    return await facultad_crud.listar_facultades(session)


async def buscar_facultad_por_id_service(session: AsyncSession, facultad_id: int) -> FacultadModel:
    facultad = await facultad_crud.buscar_facultad_por_id(session, facultad_id)
    if not facultad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe facultad con id {facultad_id}"
        )
    return facultad


async def eliminar_facultad_por_id_service(session: AsyncSession, facultad_id: int) -> None:
    facultad = await facultad_crud.buscar_facultad_por_id(session, facultad_id)
    if not facultad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe facultad con id {facultad_id}"
        )
    eliminado = await facultad_crud.eliminar_facultad_por_id(session, facultad_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la facultad"
        )
    await session.commit()


async def editar_facultad_por_id_service(session: AsyncSession, facultad_id: int, facultad_actualizar: FacultadActualizar):
    facultad = await facultad_crud.buscar_facultad_por_id(session, facultad_id)
    if not facultad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe facultad con id {facultad_id}"
        )
    actualizado = await facultad_crud.editar_facultad_por_id(session, facultad_id, facultad_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la facultad"
        )
    await session.commit()
    return await facultad_crud.buscar_facultad_por_id(session, facultad_id)
