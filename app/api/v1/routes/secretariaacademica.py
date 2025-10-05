from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import secretariaacademica as secretaria_service
from app.schemas.secretariaacademica import (
    SecretariaAcademicaCrear,
    SecretariaAcademica,
    SecretariaAcademicaActualizar,
)

router = APIRouter()


@router.post("/", response_model=SecretariaAcademica)
async def crear_secretaria(secretaria: SecretariaAcademicaCrear, session: AsyncSession = Depends(get_session)):
    return await secretaria_service.crear_secretariaacademica_service(session, secretaria)


@router.get("/", response_model=List[SecretariaAcademica], status_code=status.HTTP_200_OK)
async def listar_secretarias(session: AsyncSession = Depends(get_session)):
    return await secretaria_service.listar_secretariasacademicas_service(session)


@router.get("/{secretaria_id}", response_model=SecretariaAcademica, status_code=status.HTTP_200_OK)
async def obtener_secretaria_por_id(secretaria_id: int, session: AsyncSession = Depends(get_session)):
    return await secretaria_service.buscar_secretariaacademica_por_id_service(session, secretaria_id)


@router.delete("/{secretaria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_secretaria_por_id(secretaria_id: int, session: AsyncSession = Depends(get_session)):
    await secretaria_service.eliminar_secretariaacademica_por_id_service(session, secretaria_id)
    return


@router.patch("/{secretaria_id}", response_model=SecretariaAcademica, status_code=status.HTTP_200_OK)
async def editar_secretaria_por_id(
    secretaria_id: int,
    secretaria_actualizar: SecretariaAcademicaActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await secretaria_service.editar_secretariaacademica_por_id_service(
        session, secretaria_id, secretaria_actualizar
    )
