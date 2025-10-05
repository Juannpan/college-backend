from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import estudiante as estudiante_crud
from app.models.estudiante import EstudianteModel
from app.schemas.estudiante import EstudianteCrear, EstudianteActualizar


async def crear_estudiante_service(session: AsyncSession, nuevo_estudiante: EstudianteCrear) -> EstudianteModel:
    try:
        return await estudiante_crud.crear_estudiante(session, nuevo_estudiante)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un estudiante con ese ID."
        ) from e


async def listar_estudiantes_service(session: AsyncSession) -> Sequence[EstudianteModel]:
    return await estudiante_crud.listar_estudiantes(session)


async def buscar_estudiante_por_id_service(session: AsyncSession, estudiante_id: int) -> EstudianteModel:
    estudiante = await estudiante_crud.buscar_estudiante_por_id(session, estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe estudiante con id {estudiante_id}"
        )
    return estudiante


async def eliminar_estudiante_por_id_service(session: AsyncSession, estudiante_id: int) -> None:
    estudiante = await estudiante_crud.buscar_estudiante_por_id(session, estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe estudiante con id {estudiante_id}"
        )
    eliminado = await estudiante_crud.eliminar_estudiante_por_id(session, estudiante_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el estudiante"
        )
    await session.commit()


async def editar_estudiante_por_id_service(session: AsyncSession, estudiante_id: int, estudiante_actualizar: EstudianteActualizar):
    estudiante = await estudiante_crud.buscar_estudiante_por_id(session, estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe estudiante con id {estudiante_id}"
        )
    actualizado = await estudiante_crud.editar_estudiante_por_id(session, estudiante_id, estudiante_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar el estudiante"
        )
    await session.commit()
    return await estudiante_crud.buscar_estudiante_por_id(session, estudiante_id)
