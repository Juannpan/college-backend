from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import programa as programa_service
from app.schemas.programa import ProgramaCrear, Programa, ProgramaActualizar

router = APIRouter()


@router.post("/", response_model=Programa)
async def crear_programa(programa: ProgramaCrear, session: AsyncSession = Depends(get_session)):
    return await programa_service.crear_programa_service(session, programa)


@router.get("/", response_model=List[Programa], status_code=status.HTTP_200_OK)
async def listar_programas(session: AsyncSession = Depends(get_session)):
    return await programa_service.listar_programas_service(session)


@router.get("/{programa_id}", response_model=Programa, status_code=status.HTTP_200_OK)
async def obtener_programa_por_id(programa_id: int, session: AsyncSession = Depends(get_session)):
    return await programa_service.buscar_programa_por_id_service(session, programa_id)


@router.delete("/{programa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_programa_por_id(programa_id: int, session: AsyncSession = Depends(get_session)):
    await programa_service.eliminar_programa_por_id_service(session, programa_id)
    return


@router.patch("/{programa_id}", response_model=Programa, status_code=status.HTTP_200_OK)
async def editar_programa_por_id(
    programa_id: int,
    programa_actualizar: ProgramaActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await programa_service.editar_programa_por_id_service(
        session, programa_id, programa_actualizar
    )
