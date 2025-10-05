from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import organizacionparticipacion as org_part_crud
from app.models.organizacionparticipacion import OrganizacionParticipacionModel
from app.schemas.organizacionparticipacion import (
    OrganizacionParticipacionCrear,
    OrganizacionParticipacionActualizar,
)


async def crear_organizacionparticipacion_service(
    session: AsyncSession, nueva_participacion: OrganizacionParticipacionCrear
) -> OrganizacionParticipacionModel:
    try:
        return await org_part_crud.crear_organizacionparticipacion(session, nueva_participacion)
    except IntegrityError as e:
        # FK inválida (evento u organización no existen) -> errno 1452
        msg = str(e.orig).lower() if getattr(e, "orig", None) else ""
        if "foreign key" in msg or "1452" in msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La organización o el evento indicado no existe (violación de llave foránea).",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo crear la participación externa.",
        ) from e


async def listar_organizacionparticipaciones_service(session: AsyncSession) -> Sequence[OrganizacionParticipacionModel]:
    return await org_part_crud.listar_organizacionparticipaciones(session)


async def buscar_organizacionparticipacion_por_id_service(
    session: AsyncSession, org_part_id: int
) -> OrganizacionParticipacionModel:
    registro = await org_part_crud.buscar_organizacionparticipacion_por_id(session, org_part_id)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe participación externa con id {org_part_id}",
        )
    return registro


async def eliminar_organizacionparticipacion_por_id_service(session: AsyncSession, org_part_id: int) -> None:
    registro = await org_part_crud.buscar_organizacionparticipacion_por_id(session, org_part_id)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe participación externa con id {org_part_id}",
        )
    ok = await org_part_crud.eliminar_organizacionparticipacion_por_id(session, org_part_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la participación externa.",
        )


async def editar_organizacionparticipacion_por_id_service(
    session: AsyncSession, org_part_id: int, org_part_actualizar: OrganizacionParticipacionActualizar
) -> OrganizacionParticipacionModel:
    registro = await org_part_crud.buscar_organizacionparticipacion_por_id(session, org_part_id)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe participación externa con id {org_part_id}",
        )
    ok = await org_part_crud.editar_organizacionparticipacion_por_id(session, org_part_id, org_part_actualizar)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la participación externa.",
        )
    return await org_part_crud.buscar_organizacionparticipacion_por_id(session, org_part_id)

