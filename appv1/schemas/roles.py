from pydantic import BaseModel, StringConstraints
from datetime import datetime
from typing import Annotated

class RolesBase(BaseModel):
    rol_name: Annotated[str, StringConstraints(max_length=15)]
    

class RolesCreate(RolesBase):
    rol_name: Annotated[str, StringConstraints(max_length=15)]

class RolesResponse(RolesBase):
    rol_name: Annotated[str, StringConstraints(max_length=15)]

    
