from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import unidad as unidad_service
from app.schemas.unidad import UnidadCrear, Unidad, UnidadActualizar

router = APIRouter()


@router.post("/", response_model=Unidad)
async def crear_unidad(unidad: UnidadCrear, session: AsyncSession = Depends(get_session)):
    return await unidad_service.crear_unidad_service(session, unidad)


@router.get("/", response_model=List[Unidad], status_code=status.HTTP_200_OK)
async def listar_unidades(session: AsyncSession = Depends(get_session)):
    return await unidad_service.listar_unidades_service(session)


@router.get("/{unidad_id}", response_model=Unidad, status_code=status.HTTP_200_OK)
async def obtener_unidad_por_id(unidad_id: int, session: AsyncSession = Depends(get_session)):
    return await unidad_service.buscar_unidad_por_id_service(session, unidad_id)


@router.delete("/{unidad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_unidad_por_id(unidad_id: int, session: AsyncSession = Depends(get_session)):
    await unidad_service.eliminar_unidad_por_id_service(session, unidad_id)
    return


@router.patch("/{unidad_id}", response_model=Unidad, status_code=status.HTTP_200_OK)
async def editar_unidad_por_id(
    unidad_id: int,
    unidad_actualizar: UnidadActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await unidad_service.editar_unidad_por_id_service(
        session, unidad_id, unidad_actualizar
    )
