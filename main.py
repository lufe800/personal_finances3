from fastapi import FastAPI
from appv1.routers import category, roles, users, login
#from appv1.schemas.user import UserCreate
from db.database import test_db_connection
from fastapi.middleware.cors import CORSMiddleware


    
app = FastAPI()

#Incluir  en el objeto app los router
app.include_router(users.router,prefix="/users", tags=["users"])
app.include_router(roles.router,prefix="/roles", tags=["roles"])
app.include_router(category.router,prefix="/category", tags=["categories"])
app.include_router(login.router, prefix="/access", tags=["access"])

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)


@app.on_event("startup")
def on_startup():
    test_db_connection()


@app.get("/")
def read_root():
    return {
                "message": "Hello Word",
                
            }
    





