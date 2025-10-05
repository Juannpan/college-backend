from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import instalacion as instalacion_service
from app.schemas.instalacion import InstalacionCrear, Instalacion, InstalacionActualizar

router = APIRouter()


@router.post("/", response_model=Instalacion)
async def crear_instalacion(instalacion: InstalacionCrear, session: AsyncSession = Depends(get_session)):
    return await instalacion_service.crear_instalacion_service(session, instalacion)


@router.get("/", response_model=List[Instalacion], status_code=status.HTTP_200_OK)
async def listar_instalaciones(session: AsyncSession = Depends(get_session)):
    return await instalacion_service.listar_instalaciones_service(session)


@router.get("/{instalacion_id}", response_model=Instalacion, status_code=status.HTTP_200_OK)
async def obtener_instalacion_por_id(instalacion_id: int, session: AsyncSession = Depends(get_session)):
    return await instalacion_service.buscar_instalacion_por_id_service(session, instalacion_id)


@router.delete("/{instalacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_instalacion_por_id(instalacion_id: int, session: AsyncSession = Depends(get_session)):
    await instalacion_service.eliminar_instalacion_por_id_service(session, instalacion_id)
    return


@router.patch("/{instalacion_id}", response_model=Instalacion, status_code=status.HTTP_200_OK)
async def editar_instalacion_por_id(
    instalacion_id: int,
    instalacion_actualizar: InstalacionActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await instalacion_service.editar_instalacion_por_id_service(
        session, instalacion_id, instalacion_actualizar
    )
