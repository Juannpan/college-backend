from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from typing import Optional, Sequence

from app.models.persona import PersonaModel
from app.schemas.persona import PersonaCrear, PersonaActualizar

async def crear_persona(session: AsyncSession, persona_in: PersonaCrear) -> PersonaModel:
    obj = PersonaModel(**persona_in.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def listar_personas(session: AsyncSession) -> Sequence[PersonaModel]:
    stmt = select(PersonaModel).order_by(PersonaModel.idPersona)
    result = await session.execute(stmt)
    return result.scalars().all()

async def buscar_persona_por_id(session: AsyncSession, persona_id: int) -> Optional[PersonaModel]:
    stmt = select(PersonaModel).where(PersonaModel.idPersona == persona_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def eliminar_persona_por_id(session: AsyncSession, persona_id: int) -> bool:
    stmt = delete(PersonaModel).where(PersonaModel.idPersona == persona_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def editar_persona_por_id(
    session: AsyncSession,
    persona_id: int,
    persona_actualizar: PersonaActualizar
) -> bool:
    values = persona_actualizar.model_dump(exclude_unset=True)
    if not values:
        return True
    stmt = (
        update(PersonaModel)
        .where(PersonaModel.idPersona == persona_id)
        .values(**values)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
