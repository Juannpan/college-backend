from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import director as director_service
from app.schemas.director import DirectorCrear, Director, DirectorActualizar

router = APIRouter()


@router.post("/", response_model=Director)
async def crear_director(director: DirectorCrear, session: AsyncSession = Depends(get_session)):
    return await director_service.crear_director_service(session, director)


@router.get("/", response_model=List[Director], status_code=status.HTTP_200_OK)
async def listar_directores(session: AsyncSession = Depends(get_session)):
    return await director_service.listar_directores_service(session)


@router.get("/{director_id}", response_model=Director, status_code=status.HTTP_200_OK)
async def obtener_director_por_id(director_id: int, session: AsyncSession = Depends(get_session)):
    return await director_service.buscar_director_por_id_service(session, director_id)


@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_director_por_id(director_id: int, session: AsyncSession = Depends(get_session)):
    await director_service.eliminar_director_por_id_service(session, director_id)
    return


@router.patch("/{director_id}", response_model=Director, status_code=status.HTTP_200_OK)
async def editar_director_por_id(
    director_id: int,
    director_actualizar: DirectorActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await director_service.editar_director_por_id_service(session, director_id, director_actualizar)
