from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import organizacion as organizacion_service
from app.schemas.organizacion import OrganizacionCrear, Organizacion, OrganizacionActualizar

router = APIRouter()


@router.post("/", response_model=Organizacion)
async def crear_organizacion(organizacion: OrganizacionCrear, session: AsyncSession = Depends(get_session)):
    return await organizacion_service.crear_organizacion_service(session, organizacion)


@router.get("/", response_model=List[Organizacion], status_code=status.HTTP_200_OK)
async def listar_organizaciones(session: AsyncSession = Depends(get_session)):
    return await organizacion_service.listar_organizaciones_service(session)


@router.get("/{organizacion_id}", response_model=Organizacion, status_code=status.HTTP_200_OK)
async def obtener_organizacion_por_id(organizacion_id: int, session: AsyncSession = Depends(get_session)):
    return await organizacion_service.buscar_organizacion_por_id_service(session, organizacion_id)


@router.delete("/{organizacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_organizacion_por_id(organizacion_id: int, session: AsyncSession = Depends(get_session)):
    await organizacion_service.eliminar_organizacion_por_id_service(session, organizacion_id)
    return


@router.patch("/{organizacion_id}", response_model=Organizacion, status_code=status.HTTP_200_OK)
async def editar_organizacion_por_id(
    organizacion_id: int,
    organizacion_actualizar: OrganizacionActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await organizacion_service.editar_organizacion_por_id_service(
        session, organizacion_id, organizacion_actualizar
    )
