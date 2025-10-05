from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import historialcontrasenas as historial_service
from app.schemas.historialcontrasenas import (
    HistorialContrasenasCrear,
    HistorialContrasenas,
    HistorialContrasenasActualizar,
)

router = APIRouter()


@router.post("/", response_model=HistorialContrasenas)
async def crear_historial_contrasena(
    historial: HistorialContrasenasCrear,
    session: AsyncSession = Depends(get_session),
):
    return await historial_service.crear_historialcontrasenas_service(session, historial)


@router.get("/", response_model=List[HistorialContrasenas], status_code=status.HTTP_200_OK)
async def listar_historial_contrasenas(session: AsyncSession = Depends(get_session)):
    return await historial_service.listar_historialcontrasenas_service(session)


@router.get("/{historial_id}", response_model=HistorialContrasenas, status_code=status.HTTP_200_OK)
async def obtener_historial_por_id(historial_id: int, session: AsyncSession = Depends(get_session)):
    return await historial_service.buscar_historialcontrasenas_por_id_service(session, historial_id)


@router.delete("/{historial_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_historial_por_id(historial_id: int, session: AsyncSession = Depends(get_session)):
    await historial_service.eliminar_historialcontrasenas_por_id_service(session, historial_id)
    return


@router.patch("/{historial_id}", response_model=HistorialContrasenas, status_code=status.HTTP_200_OK)
async def editar_historial_por_id(
    historial_id: int,
    historial_actualizar: HistorialContrasenasActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await historial_service.editar_historialcontrasenas_por_id_service(
        session, historial_id, historial_actualizar
    )
