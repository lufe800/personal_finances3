from typing import List
from fastapi import APIRouter, Depends, HTTPException
from appv1.crud.permissions import get_permissions
from appv1.routers.login import get_current_user
from appv1.schemas.user import UserCreate, UserResponse, UserUpdate, PaginatedUsersResponse
from appv1.crud.users import create_user_sql, get_all_users, get_user_by_email, get_user_by_id, get_user_by_rol, update_user, get_all_users_paginated, delete_user
from db.database import get_db
from db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text


router = APIRouter()
MODULE = 'usuarios'

@router.post("/create")
async def insert_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_insert:
        raise HTTPException(status_code=401, detail="User not found")
    respuesta = create_user_sql(db, user)
    
    if current_user.user_role != 'SuperAdmin':
        if user.user_role == 'SuperAdmin':
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
    respuesta = create_user_sql(db, user)
    if respuesta:
        return{"mensaje":"Usuario registrado con éxito"}
    

@router.get("/get-user-by-emai/", response_model=UserResponse) #crud de la ruta para buscar usuario por email
async def read_user_by_email(
    email:str,
    db:Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if current_user.mail != email: #si el email es diferente
        if not permisos.p_select:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
    usuario = get_user_by_email(db, email)
    if usuario is None:
        raise HTTPException(status_code=404, detail="User not found")
    return usuario

@router.get("/get-all/", response_model=List[UserResponse]) #crud de la ruta para buscar usuario por email
async def read_all_users(
    db:Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_select:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    usuarios = get_all_users(db)
    if len(usuarios) == 0:
        raise HTTPException(status_code=404, detail="No hay usuarios")
    return usuarios

@router.get("/get-user-by-rol/", response_model=List[UserResponse])
async def read_user_by_rol(rol: str, db: Session= Depends(get_db)):
    usuario = get_user_by_rol(db, rol)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario con este rol no encontrado")
    return usuario

# Endpoint para actualizar un usuario
@router.put("/update/", response_model=dict)
def update_user_by_id(
    user_id: str, 
    user: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if user_id != current_user.user_id: 
        if permisos.p_update:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
    verify_user = get_user_by_id(db, user_id)
    if verify_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_user = update_user(db, user_id, user)
    if db_user:
        return {"mensaje": "registro actualizado con éxito"}

@router.delete("/delete/{user_id}", response_model=dict)
def delete_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if user_id != current_user.user_id:
        if not permisos.p_delete:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no autorizado")
    
    result = delete_user(db, user_id)
    if result:
        return {"mensaje": "Usuario eliminado con éxito"}
    
# usuarios paginados
@router.get("/users-by-page/", response_model=PaginatedUsersResponse)
def get_all_users_by_page(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    
    users, total_pages = get_all_users_paginated(db, page, page_size)

    return {
        "users": users,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size
    }
    


        