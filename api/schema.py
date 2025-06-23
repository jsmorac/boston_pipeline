# api/schema.py

from pydantic import BaseModel, Field

class HouseData(BaseModel):
    crim: float = Field(..., ge=0, description="Índice de criminalidad por zona")
    zn: float = Field(..., ge=0, description="Proporción de terrenos residenciales de gran tamaño")
    indus: float = Field(..., ge=0, le=30, description="Proporción de terrenos comerciales")
    chas: int = Field(..., ge=0, le=1, description="Limita con el río Charles (0: No, 1: Sí)")
    nox: float = Field(..., ge=0.3, le=1.0, description="Concentración de óxidos de nitrógeno")
    rm: float = Field(..., ge=3.0, le=10.0, description="Promedio de habitaciones por vivienda")
    age: float = Field(..., ge=0, le=100, description="Proporción de viviendas construidas antes de 1940")
    dis: float = Field(..., ge=1.0, description="Distancia a centros de empleo")
    rad: int = Field(..., ge=1, le=24, description="Índice de accesibilidad a autopistas")
    tax: float = Field(..., ge=100, le=800, description="Tasa de impuesto a la propiedad")
    ptratio: float = Field(..., ge=10.0, le=25.0, description="Proporción alumno/profesor")
    b: float = Field(..., ge=0, le=400, description="Medida relacionada con población afrodescendiente")
    lstat: float = Field(..., ge=0, le=40, description="% de estatus bajo de la población")
