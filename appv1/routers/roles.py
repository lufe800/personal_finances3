from http.client import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from appv1.schemas.roles import RolesCreate, RolesResponse
from appv1.crud.roles import create_roles_sql, get_rol_by_name, get_all_roles
from db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text



router = APIRouter()

@router.post("/create")
async def insert_rol(roles:RolesCreate , db: Session = Depends(get_db)):
    respuesta = create_roles_sql(db, roles)
    if respuesta:
        return{"mensaje":"Rol creado con éxito"}
    
@router.get("/get-roles-by-name/", response_model=RolesResponse) #crud de la ruta para buscar usuario por email
async def read_roles_by_name(rol_name:str, db:Session = Depends(get_db)):
    rol = get_rol_by_name(db, rol_name)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")
    return rol

@router.get("/get-all/", response_model=List[RolesResponse]) #crud de la ruta para buscar usuario por email
async def read_all_roles(db:Session = Depends(get_db)):
    roles = get_all_roles(db)
    if len(roles) == 0:
        raise HTTPException(status_code=404, detail="Roles not found")
    return roles
