from fastapi import APIRouter

# Importación de cada enrutador existente en routes
from app.api.v1.routes import (
    aprobacionevento,
    director,
    docente,
    estudiante,
    evento,
    facultad,
    historialcontrasenas,
    instalacion,
    organizacion,
    organizacionparticipacion,
    participacion,
    persona,
    programa,
    secretariaacademica,
    unidad,
)

# Crea el enrutador principal para la versión 1 de la API
api_router_v1 = APIRouter()

# Incluye cada enrutador con su prefijo y etiquetas correspondientes
api_router_v1.include_router(aprobacionevento.router, prefix="/aprobaciones-evento", tags=["Aprobaciones Evento"])
api_router_v1.include_router(director.router, prefix="/directores", tags=["Directores"])
api_router_v1.include_router(docente.router, prefix="/docentes", tags=["Docentes"])
api_router_v1.include_router(estudiante.router, prefix="/estudiantes", tags=["Estudiantes"])
api_router_v1.include_router(evento.router, prefix="/eventos", tags=["Eventos"])
api_router_v1.include_router(facultad.router, prefix="/facultades", tags=["Facultades"])
api_router_v1.include_router(historialcontrasenas.router, prefix="/historial-contrasenas", tags=["Historial de Contraseñas"])
api_router_v1.include_router(instalacion.router, prefix="/instalaciones", tags=["Instalaciones"])
api_router_v1.include_router(organizacion.router, prefix="/organizaciones", tags=["Organizaciones"])
api_router_v1.include_router(organizacionparticipacion.router, prefix="/organizacion-participacion", tags=["Organización Participación"])
api_router_v1.include_router(participacion.router, prefix="/participaciones", tags=["Participaciones"])
api_router_v1.include_router(persona.router, prefix="/personas", tags=["Personas"])
api_router_v1.include_router(programa.router, prefix="/programas", tags=["Programas"])
api_router_v1.include_router(secretariaacademica.router, prefix="/secretarias-academicas", tags=["Secretarías Académicas"])
api_router_v1.include_router(unidad.router, prefix="/unidades", tags=["Unidades"])
