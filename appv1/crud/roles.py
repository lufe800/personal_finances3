from http.client import HTTPException
from sqlite3 import IntegrityError
from sqlalchemy import text
from sqlalchemy.orm import Session
from appv1.schemas.roles import RolesCreate
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


# Crear un rol
def create_roles_sql(db: Session, roles: RolesCreate):
    try:
        sql_query = text(
        "INSERT INTO roles (rol_name) "
        "VALUES (:rol_name)"
        )
        db.execute(sql_query,{"rol_name": roles.rol_name})
        db.commit()
        return True  # Retorna True si la inserción fue exitosa
    
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al crear rol: {e}")
        if 'Duplicate entry' in str(e.orig):
            if 'PRIMARY' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. El rol ingresado ya está en uso")
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear usuario")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear rol: {e}")
        raise HTTPException(status_code=500, detail="Error al crear rol") ## si no es exitosa retorna false
    
def get_rol_by_name(db: Session, p_name: str):
    try:
        sql = text("SELECT * FROM roles WHERE rol_name = :name")
        result = db.execute(sql, {"name": p_name}).fetchone()
        return result
    except  SQLAlchemyError as e:
        print(f"Error al buscar rol por nombre: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar rol por nombre")
    
def get_all_roles(db: Session):
    try:
        sql = text("SELECT * FROM roles")
        result = db.execute(sql).fetchall()
        return result
    except  SQLAlchemyError as e:
        print(f"Error al buscar roles: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar roles") 