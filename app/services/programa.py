from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import programa as programa_crud
from app.models.programa import ProgramaModel
from app.schemas.programa import ProgramaCrear, ProgramaActualizar


async def crear_programa_service(session: AsyncSession, nuevo_programa: ProgramaCrear) -> ProgramaModel:
    try:
        return await programa_crud.crear_programa(session, nuevo_programa)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un programa con ese código."
        ) from e


async def listar_programas_service(session: AsyncSession) -> Sequence[ProgramaModel]:
    return await programa_crud.listar_programas(session)


async def buscar_programa_por_id_service(session: AsyncSession, programa_id: int) -> ProgramaModel:
    programa = await programa_crud.buscar_programa_por_id(session, programa_id)
    if not programa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe programa con id {programa_id}"
        )
    return programa


async def eliminar_programa_por_id_service(session: AsyncSession, programa_id: int) -> None:
    programa = await programa_crud.buscar_programa_por_id(session, programa_id)
    if not programa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe programa con id {programa_id}"
        )
    eliminado = await programa_crud.eliminar_programa_por_id(session, programa_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el programa"
        )
    await session.commit()


async def editar_programa_por_id_service(session: AsyncSession, programa_id: int, programa_actualizar: ProgramaActualizar):
    programa = await programa_crud.buscar_programa_por_id(session, programa_id)
    if not programa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe programa con id {programa_id}"
        )
    actualizado = await programa_crud.editar_programa_por_id(session, programa_id, programa_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar el programa"
        )
    await session.commit()
    return await programa_crud.buscar_programa_por_id(session, programa_id)
