from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import persona as persona_service
from app.schemas.persona import PersonaCrear, Persona, PersonaActualizar

router = APIRouter()


@router.post("/", response_model=Persona)
async def crear_persona(persona: PersonaCrear, session: AsyncSession = Depends(get_session)):
    return await persona_service.crear_persona_service(session, persona)


@router.get("/", response_model=List[Persona], status_code=status.HTTP_200_OK)
async def listar_personas(session: AsyncSession = Depends(get_session)):
    return await persona_service.listar_personas_service(session)


@router.get("/{persona_id}", response_model=Persona, status_code=status.HTTP_200_OK)
async def obtener_persona_por_id(persona_id: int, session: AsyncSession = Depends(get_session)):
    return await persona_service.buscar_persona_por_id_service(session, persona_id)


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_persona_por_id(persona_id: int, session: AsyncSession = Depends(get_session)):
    await persona_service.eliminar_persona_por_id_service(session, persona_id)
    return


@router.patch("/{persona_id}", response_model=Persona, status_code=status.HTTP_200_OK)
async def editar_persona_por_id(
    persona_id: int,
    persona_actualizar: PersonaActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await persona_service.editar_persona_por_id_service(
        session, persona_id, persona_actualizar
    )
