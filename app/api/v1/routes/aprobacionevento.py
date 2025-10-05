from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import aprobacionevento as aprobacionevento_service
from app.schemas.aprobacionevento import (
    AprobacionEventoCrear,
    AprobacionEvento,
    AprobacionEventoActualizar,
)

router = APIRouter()


@router.post("/", response_model=AprobacionEvento)
async def crear_aprobacion(
    aprobacion: AprobacionEventoCrear,
    session: AsyncSession = Depends(get_session),
):
    return await aprobacionevento_service.crear_aprobacionevento_service(session, aprobacion)


@router.get("/", response_model=List[AprobacionEvento], status_code=status.HTTP_200_OK)
async def listar_aprobaciones(session: AsyncSession = Depends(get_session)):
    return await aprobacionevento_service.listar_aprobacionevento_service(session)


@router.get("/{aprobacion_id}", response_model=AprobacionEvento, status_code=status.HTTP_200_OK)
async def obtener_aprobacion_por_id(aprobacion_id: int, session: AsyncSession = Depends(get_session)):
    return await aprobacionevento_service.buscar_aprobacionevento_por_id_service(session, aprobacion_id)


@router.delete("/{aprobacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_aprobacion_por_id(aprobacion_id: int, session: AsyncSession = Depends(get_session)):
    await aprobacionevento_service.eliminar_aprobacionevento_por_id_service(session, aprobacion_id)
    return


@router.patch("/{aprobacion_id}", response_model=AprobacionEvento, status_code=status.HTTP_200_OK)
async def editar_aprobacion_por_id(
    aprobacion_id: int,
    aprobacion_actualizar: AprobacionEventoActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await aprobacionevento_service.editar_aprobacionevento_por_id_service(
        session, aprobacion_id, aprobacion_actualizar
    )
