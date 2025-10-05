from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import docente as docente_service
from app.schemas.docente import DocenteCrear, Docente, DocenteActualizar

router = APIRouter()


@router.post("/", response_model=Docente)
async def crear_docente(docente: DocenteCrear, session: AsyncSession = Depends(get_session)):
    return await docente_service.crear_docente_service(session, docente)


@router.get("/", response_model=List[Docente], status_code=status.HTTP_200_OK)
async def listar_docentes(session: AsyncSession = Depends(get_session)):
    return await docente_service.listar_docentes_service(session)


@router.get("/{docente_id}", response_model=Docente, status_code=status.HTTP_200_OK)
async def obtener_docente_por_id(docente_id: int, session: AsyncSession = Depends(get_session)):
    return await docente_service.buscar_docente_por_id_service(session, docente_id)


@router.delete("/{docente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_docente_por_id(docente_id: int, session: AsyncSession = Depends(get_session)):
    await docente_service.eliminar_docente_por_id_service(session, docente_id)
    return


@router.patch("/{docente_id}", response_model=Docente, status_code=status.HTTP_200_OK)
async def editar_docente_por_id(
    docente_id: int,
    docente_actualizar: DocenteActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await docente_service.editar_docente_por_id_service(session, docente_id, docente_actualizar)
