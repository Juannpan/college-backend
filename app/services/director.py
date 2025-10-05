from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import director as director_crud
from app.models.director import DirectorModel
from app.schemas.director import DirectorCrear, DirectorActualizar


async def crear_director_service(session: AsyncSession, nuevo_director: DirectorCrear) -> DirectorModel:
    try:
        return await director_crud.crear_director(session, nuevo_director)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un director con ese ID."
        ) from e


async def listar_directores_service(session: AsyncSession) -> Sequence[DirectorModel]:
    return await director_crud.listar_directores(session)


async def buscar_director_por_id_service(session: AsyncSession, director_id: int) -> DirectorModel:
    director = await director_crud.buscar_director_por_id(session, director_id)
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe director con id {director_id}"
        )
    return director


async def eliminar_director_por_id_service(session: AsyncSession, director_id: int) -> None:
    director = await director_crud.buscar_director_por_id(session, director_id)
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe director con id {director_id}"
        )
    eliminado = await director_crud.eliminar_director_por_id(session, director_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el director"
        )
    await session.commit()


async def editar_director_por_id_service(session: AsyncSession, director_id: int, director_actualizar: DirectorActualizar):
    director = await director_crud.buscar_director_por_id(session, director_id)
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe director con id {director_id}"
        )
    actualizado = await director_crud.editar_director_por_id(session, director_id, director_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar el director"
        )
    await session.commit()
    return await director_crud.buscar_director_por_id(session, director_id)
