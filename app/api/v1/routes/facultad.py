from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import facultad as facultad_service
from app.schemas.facultad import FacultadCrear, Facultad, FacultadActualizar

router = APIRouter()


@router.post("/", response_model=Facultad)
async def crear_facultad(facultad: FacultadCrear, session: AsyncSession = Depends(get_session)):
    return await facultad_service.crear_facultad_service(session, facultad)


@router.get("/", response_model=List[Facultad], status_code=status.HTTP_200_OK)
async def listar_facultades(session: AsyncSession = Depends(get_session)):
    return await facultad_service.listar_facultades_service(session)


@router.get("/{facultad_id}", response_model=Facultad, status_code=status.HTTP_200_OK)
async def obtener_facultad_por_id(facultad_id: int, session: AsyncSession = Depends(get_session)):
    return await facultad_service.buscar_facultad_por_id_service(session, facultad_id)


@router.delete("/{facultad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_facultad_por_id(facultad_id: int, session: AsyncSession = Depends(get_session)):
    await facultad_service.eliminar_facultad_por_id_service(session, facultad_id)
    return


@router.patch("/{facultad_id}", response_model=Facultad, status_code=status.HTTP_200_OK)
async def editar_facultad_por_id(
    facultad_id: int,
    facultad_actualizar: FacultadActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await facultad_service.editar_facultad_por_id_service(session, facultad_id, facultad_actualizar)
