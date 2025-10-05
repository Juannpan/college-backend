from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import organizacionparticipacion as org_part_service
from app.schemas.organizacionparticipacion import (
    OrganizacionParticipacionCrear,
    OrganizacionParticipacion,
    OrganizacionParticipacionActualizar,
)

router = APIRouter()


@router.post("/", response_model=OrganizacionParticipacion)
async def crear_organizacion_participacion(
    org_part: OrganizacionParticipacionCrear,
    session: AsyncSession = Depends(get_session),
):
    return await org_part_service.crear_organizacionparticipacion_service(session, org_part)


@router.get("/", response_model=List[OrganizacionParticipacion], status_code=status.HTTP_200_OK)
async def listar_organizacion_participaciones(session: AsyncSession = Depends(get_session)):
    return await org_part_service.listar_organizacionparticipaciones_service(session)


@router.get("/{org_part_id}", response_model=OrganizacionParticipacion, status_code=status.HTTP_200_OK)
async def obtener_org_part_por_id(org_part_id: int, session: AsyncSession = Depends(get_session)):
    return await org_part_service.buscar_organizacionparticipacion_por_id_service(session, org_part_id)


@router.delete("/{org_part_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_org_part_por_id(org_part_id: int, session: AsyncSession = Depends(get_session)):
    await org_part_service.eliminar_organizacionparticipacion_por_id_service(session, org_part_id)
    return


@router.patch("/{org_part_id}", response_model=OrganizacionParticipacion, status_code=status.HTTP_200_OK)
async def editar_org_part_por_id(
    org_part_id: int,
    org_part_actualizar: OrganizacionParticipacionActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await org_part_service.editar_organizacionparticipacion_por_id_service(
        session, org_part_id, org_part_actualizar
    )
