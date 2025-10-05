from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import secretariaacademica as secretaria_crud
from app.models.secretariaacademica import SecretariaAcademicaModel
from app.schemas.secretariaacademica import SecretariaAcademicaCrear, SecretariaAcademicaActualizar


async def crear_secretaria_service(session: AsyncSession, nueva_secretaria: SecretariaAcademicaCrear) -> SecretariaAcademicaModel:
    try:
        return await secretaria_crud.crear_secretaria(session, nueva_secretaria)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una secretaria académica con ese ID."
        ) from e


async def listar_secretarias_service(session: AsyncSession) -> Sequence[SecretariaAcademicaModel]:
    return await secretaria_crud.listar_secretarias(session)


async def buscar_secretaria_por_id_service(session: AsyncSession, secretaria_id: int) -> SecretariaAcademicaModel:
    secretaria = await secretaria_crud.buscar_secretaria_por_id(session, secretaria_id)
    if not secretaria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe secretaria académica con id {secretaria_id}"
        )
    return secretaria


async def eliminar_secretaria_por_id_service(session: AsyncSession, secretaria_id: int) -> None:
    secretaria = await secretaria_crud.buscar_secretaria_por_id(session, secretaria_id)
    if not secretaria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe secretaria académica con id {secretaria_id}"
        )
    eliminado = await secretaria_crud.eliminar_secretaria_por_id(session, secretaria_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la secretaria académica"
        )
    await session.commit()


async def editar_secretaria_por_id_service(session: AsyncSession, secretaria_id: int, secretaria_actualizar: SecretariaAcademicaActualizar):
    secretaria = await secretaria_crud.buscar_secretaria_por_id(session, secretaria_id)
    if not secretaria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe secretaria académica con id {secretaria_id}"
        )
    actualizado = await secretaria_crud.editar_secretaria_por_id(session, secretaria_id, secretaria_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la secretaria académica"
        )
    await session.commit()
    return await secretaria_crud.buscar_secretaria_por_id(session, secretaria_id)
