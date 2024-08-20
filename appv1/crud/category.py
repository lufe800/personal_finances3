from http.client import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from appv1.schemas.category import CategoryCreate

# Crear un categoria
def create_category_sql(db: Session, category: CategoryCreate):
    try:
        
        sql_query = text(
            "INSERT INTO category (category_name, category_description, category_status) "
            "VALUES (:category_name, :category_description, :category_status)"
        )
        params = {
            "category_name": category.category_name,
            "category_description": category.category_description,
            "category_status":category.category_status,

        }
        db.execute(sql_query, params)
        db.commit()
        return True  # Retorna True si la inserción fue exitosa
    
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al crear categoria: {e}")
        if 'Duplicate entry' in str(e.orig):
            if 'PRIMARY' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. El ID de categoria ya está en uso")
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear categoria")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear categoria: {e}")
        raise HTTPException(status_code=500, detail="Error al crear usuario") ## si no es exitosa retorna false
    
# Consultar un categoria por su nombre
def get_category_by_name(db: Session, p_name: str):
    try:
        sql = text("SELECT * FROM category WHERE category_name = :category_name")
        result = db.execute(sql, {"category_name": p_name}).fetchone()
        return result
    except  SQLAlchemyError as e:
        print(f"Error al buscar categoria por nombre: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar categoria por nombre")
    
    
# Consultar todos las categorias
def get_all_categorys(db: Session):
    try:
        sql = text("SELECT * FROM category WHERE category_status = true")
        result = db.execute(sql).fetchall()
        return result
    except  SQLAlchemyError as e:
        print(f"Error al buscar categorias: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar categorias")