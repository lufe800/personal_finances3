from pydantic import BaseModel, StringConstraints
from typing import Annotated

class CategoryBase(BaseModel):
    category_name: Annotated[str, StringConstraints(max_length=50)]
    category_description: Annotated[str, StringConstraints(max_length=120)]
    category_status: Annotated[int, StringConstraints(max_length=1)]

class CategoryCreate(CategoryBase):
    category_name: Annotated[str, StringConstraints(max_length=50)]
    category_description: Annotated[str, StringConstraints(max_length=120)]
    category_status: bool = True
    
class CategoryResponse(CategoryBase):
    category_status: bool = True


