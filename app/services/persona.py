from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import persona as persona_crud
from app.models.persona import PersonaModel
from app.schemas.persona import PersonaCrear, PersonaActualizar


async def crear_persona_service(session: AsyncSession, nueva_persona: PersonaCrear) -> PersonaModel:
    try:
        return await persona_crud.crear_persona(session, nueva_persona)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una persona con esa identificación."
        ) from e


async def listar_personas_service(session: AsyncSession) -> Sequence[PersonaModel]:
    return await persona_crud.listar_personas(session)


async def buscar_persona_por_id_service(session: AsyncSession, persona_id: int) -> PersonaModel:
    persona = await persona_crud.buscar_persona_por_id(session, persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe persona con id {persona_id}"
        )
    return persona


async def eliminar_persona_por_id_service(session: AsyncSession, persona_id: int) -> None:
    persona = await persona_crud.buscar_persona_por_id(session, persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe persona con id {persona_id}"
        )
    eliminado = await persona_crud.eliminar_persona_por_id(session, persona_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la persona"
        )
    await session.commit()


async def editar_persona_por_id_service(session: AsyncSession, persona_id: int, persona_actualizar: PersonaActualizar):
    persona = await persona_crud.buscar_persona_por_id(session, persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe persona con id {persona_id}"
        )
    actualizado = await persona_crud.editar_persona_por_id(session, persona_id, persona_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la persona"
        )
    await session.commit()
    return await persona_crud.buscar_persona_por_id(session, persona_id)
