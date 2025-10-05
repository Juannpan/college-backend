from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import evento as evento_service
from app.schemas.evento import EventoCrear, Evento, EventoActualizar

router = APIRouter()


@router.post("/", response_model=Evento)
async def crear_evento(evento: EventoCrear, session: AsyncSession = Depends(get_session)):
    return await evento_service.crear_evento_service(session, evento)


@router.get("/", response_model=List[Evento], status_code=status.HTTP_200_OK)
async def listar_eventos(session: AsyncSession = Depends(get_session)):
    return await evento_service.listar_eventos_service(session)


@router.get("/{evento_id}", response_model=Evento, status_code=status.HTTP_200_OK)
async def obtener_evento_por_id(evento_id: int, session: AsyncSession = Depends(get_session)):
    return await evento_service.buscar_evento_por_id_service(session, evento_id)


@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_evento_por_id(evento_id: int, session: AsyncSession = Depends(get_session)):
    await evento_service.eliminar_evento_por_id_service(session, evento_id)
    return


@router.patch("/{evento_id}", response_model=Evento, status_code=status.HTTP_200_OK)
async def editar_evento_por_id(
    evento_id: int,
    evento_actualizar: EventoActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await evento_service.editar_evento_por_id_service(session, evento_id, evento_actualizar)
