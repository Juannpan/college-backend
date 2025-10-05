from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.crud import docente as docente_crud
from app.models.docente import DocenteModel
from app.schemas.docente import DocenteCrear, DocenteActualizar


async def crear_docente_service(session: AsyncSession, nuevo_docente: DocenteCrear) -> DocenteModel:
    try:
        return await docente_crud.crear_docente(session, nuevo_docente)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un docente con ese ID."
        ) from e


async def listar_docentes_service(session: AsyncSession) -> Sequence[DocenteModel]:
    return await docente_crud.listar_docentes(session)


async def buscar_docente_por_id_service(session: AsyncSession, docente_id: int) -> DocenteModel:
    docente = await docente_crud.buscar_docente_por_id(session, docente_id)
    if not docente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe docente con id {docente_id}"
        )
    return docente


async def eliminar_docente_por_id_service(session: AsyncSession, docente_id: int) -> None:
    docente = await docente_crud.buscar_docente_por_id(session, docente_id)
    if not docente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe docente con id {docente_id}"
        )
    eliminado = await docente_crud.eliminar_docente_por_id(session, docente_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar el docente"
        )
    await session.commit()


async def editar_docente_por_id_service(session: AsyncSession, docente_id: int, docente_actualizar: DocenteActualizar):
    docente = await docente_crud.buscar_docente_por_id(session, docente_id)
    if not docente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe docente con id {docente_id}"
        )
    actualizado = await docente_crud.editar_docente_por_id(session, docente_id, docente_actualizar)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar el docente"
        )
    await session.commit()
    return await docente_crud.buscar_docente_por_id(session, docente_id)
