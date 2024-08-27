from http.client import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


# Consultar permisos de un rol por modulo
def get_permissions(db: Session, rol: str, module: str):
    try:
        sql = text("SELECT p_select, p_insert, p_update, p_delete FROM permissions WHERE rol_name = :rol AND module_name = :module")
        result = db.execute(sql, {"rol": rol, "module": module}).fetchone()
        return result
    except  SQLAlchemyError as e:
        print(f"Error al buscar usuario por : {e}")
        raise HTTPException(status_code=500, detail="Error al buscar usuario por email")
    

# Consultar  todos los permisos de un rol por modulo
def get_all_permissions(db: Session, rol: str):
    try:
        sql = text("SELECT p_select, module_name FROM permissions WHERE rol_name = :rol")
        result = db.execute(sql, {"rol": rol}).fetchall()
        return result
    except  SQLAlchemyError as e:
        print(f"Error al buscar usuario por : {e}")
        raise HTTPException(status_code=500, detail="Error al buscar usuario por email")
    