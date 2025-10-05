from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import instalacion as instalacion_crud
from app.models.instalacion import InstalacionModel
from app.schemas.instalacion import InstalacionCrear, InstalacionActualizar


async def crear_instalacion_service(session: AsyncSession, nueva_instalacion: InstalacionCrear) -> InstalacionModel:
    try:
        return await instalacion_crud.crear_instalacion(session, nueva_instalacion)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una instalación con ese ID."
        ) from e


async def listar_instalaciones_service(session: AsyncSession) -> Sequence[InstalacionModel]:
    return await instalacion_crud.listar_instalaciones(session)


async def buscar_instalacion_por_id_service(session: AsyncSession, instalacion_id: int) -> InstalacionModel:
    instalacion = await instalacion_crud.buscar_instalacion_por_id(session, instalacion_id)
    if not instalacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe instalación con id {instalacion_id}"
        )
    return instalacion


async def eliminar_instalacion_por_id_service(session: AsyncSession, instalacion_id: int) -> None:
    instalacion = await instalacion_crud.buscar_instalacion_por_id(session, instalacion_id)
    if not instalacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe instalación con id {instalacion_id}"
        )
    eliminado = await instalacion_crud.eliminar_instalacion_por_id(session, instalacion_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la instalación"
        )
    await session.commit()


async def editar_instalacion_por_id_service(session: AsyncSession, instalacion_id: int, instalacion_actualizar: InstalacionActualizar):
    instalacion = await instalacion_crud.buscar_instalacion_por_id(session, instalacion_id)
    if not instalacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe instalación con id {instalacion_id}"
        )
    actualizado = await instalacion_crud.editar_instalacion_por_id(session, instalacion_id, instalacion_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la instalación"
        )
    await session.commit()
    return await instalacion_crud.buscar_instalacion_por_id(session, instalacion_id)

