from typing import List
from fastapi import APIRouter, Depends, HTTPException
from appv1.schemas.category import CategoryCreate, CategoryResponse
from appv1.crud.category import create_category_sql, get_all_categorys, get_category_by_name
from db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text


router = APIRouter()

@router.post("/create")
async def insert_category(category: CategoryCreate, db: Session = Depends(get_db)):
    respuesta = create_category_sql(db, category)
    if respuesta:
        return{"mensaje":"Categoria creada con éxito"}

@router.get("/get-category-by-name/", response_model=CategoryResponse) #crud de la ruta para buscar usuario por email
async def read_category_by_name(name:str, db:Session = Depends(get_db)):
    category = get_category_by_name(db, name)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/get-all/", response_model=List[CategoryResponse]) #crud de la ruta para buscar usuario por email
async def read_all_category(db:Session = Depends(get_db)):
    category = get_all_categorys(db)
    if len(category) == 0:
        raise HTTPException(status_code=404, detail="Categorys not found")
    return category