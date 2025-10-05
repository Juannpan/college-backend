from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import historialcontrasenas as historial_crud
from app.models.historialcontrasenas import HistorialContrasenasModel
from app.schemas.historialcontrasenas import HistorialContrasenasCrear, HistorialContrasenasActualizar

# Nombres que tu router está llamando:
# - crear_historialcontrasenas_service
# - listar_historialcontrasenas_service
# - buscar_historialcontrasenas_por_id_service
# - eliminar_historialcontrasenas_por_id_service
# - editar_historialcontrasenas_por_id_service

async def crear_historialcontrasenas_service(session: AsyncSession, nuevo_registro: HistorialContrasenasCrear) -> HistorialContrasenasModel:
    try:
        # En el CRUD el nombre es crear_historial_contrasena
        return await historial_crud.crear_historial_contrasena(session, nuevo_registro)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al registrar la contraseña en el historial."
        ) from e

async def listar_historialcontrasenas_service(session: AsyncSession) -> Sequence[HistorialContrasenasModel]:
    return await historial_crud.listar_historial_contrasenas(session)

async def buscar_historialcontrasenas_por_id_service(session: AsyncSession, historial_id: int) -> HistorialContrasenasModel:
    registro = await historial_crud.buscar_historial_por_id(session, historial_id)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe historial con id {historial_id}"
        )
    return registro

async def eliminar_historialcontrasenas_por_id_service(session: AsyncSession, historial_id: int) -> None:
    registro = await historial_crud.buscar_historial_por_id(session, historial_id)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe historial con id {historial_id}"
        )
    eliminado = await historial_crud.eliminar_historial_por_id(session, historial_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el registro del historial"
        )
    await session.commit()

async def editar_historialcontrasenas_por_id_service(session: AsyncSession, historial_id: int, historial_actualizar: HistorialContrasenasActualizar) -> HistorialContrasenasModel:
    registro = await historial_crud.buscar_historial_por_id(session, historial_id)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe historial con id {historial_id}"
        )
    actualizado = await historial_crud.editar_historial_por_id(session, historial_id, historial_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar el registro del historial"
        )
    await session.commit()
    return await historial_crud.buscar_historial_por_id(session, historial_id)

