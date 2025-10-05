from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import participacion as participacion_service
from app.schemas.participacion import ParticipacionCrear, Participacion, ParticipacionActualizar

router = APIRouter()


@router.post("/", response_model=Participacion)
async def crear_participacion(participacion: ParticipacionCrear, session: AsyncSession = Depends(get_session)):
    return await participacion_service.crear_participacion_service(session, participacion)


@router.get("/", response_model=List[Participacion], status_code=status.HTTP_200_OK)
async def listar_participaciones(session: AsyncSession = Depends(get_session)):
    return await participacion_service.listar_participaciones_service(session)


@router.get("/{participacion_id}", response_model=Participacion, status_code=status.HTTP_200_OK)
async def obtener_participacion_por_id(participacion_id: int, session: AsyncSession = Depends(get_session)):
    return await participacion_service.buscar_participacion_por_id_service(session, participacion_id)


@router.delete("/{participacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_participacion_por_id(participacion_id: int, session: AsyncSession = Depends(get_session)):
    await participacion_service.eliminar_participacion_por_id_service(session, participacion_id)
    return


@router.patch("/{participacion_id}", response_model=Participacion, status_code=status.HTTP_200_OK)
async def editar_participacion_por_id(
    participacion_id: int,
    participacion_actualizar: ParticipacionActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await participacion_service.editar_participacion_por_id_service(
        session, participacion_id, participacion_actualizar
    )
