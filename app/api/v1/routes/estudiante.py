from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.mysql import get_session
from app.services import estudiante as estudiante_service
from app.schemas.estudiante import EstudianteCrear, Estudiante, EstudianteActualizar

router = APIRouter()


@router.post("/", response_model=Estudiante)
async def crear_estudiante(estudiante: EstudianteCrear, session: AsyncSession = Depends(get_session)):
    return await estudiante_service.crear_estudiante_service(session, estudiante)


@router.get("/", response_model=List[Estudiante], status_code=status.HTTP_200_OK)
async def listar_estudiantes(session: AsyncSession = Depends(get_session)):
    return await estudiante_service.listar_estudiantes_service(session)


@router.get("/{estudiante_id}", response_model=Estudiante, status_code=status.HTTP_200_OK)
async def obtener_estudiante_por_id(estudiante_id: int, session: AsyncSession = Depends(get_session)):
    return await estudiante_service.buscar_estudiante_por_id_service(session, estudiante_id)


@router.delete("/{estudiante_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_estudiante_por_id(estudiante_id: int, session: AsyncSession = Depends(get_session)):
    await estudiante_service.eliminar_estudiante_por_id_service(session, estudiante_id)
    return


@router.patch("/{estudiante_id}", response_model=Estudiante, status_code=status.HTTP_200_OK)
async def editar_estudiante_por_id(
    estudiante_id: int,
    estudiante_actualizar: EstudianteActualizar,
    session: AsyncSession = Depends(get_session),
):
    return await estudiante_service.editar_estudiante_por_id_service(session, estudiante_id, estudiante_actualizar)
