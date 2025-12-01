from pydantic import BaseModel, Field, field_validator, constr
from typing import Annotated

class Address(BaseModel):
    street: constr(min_length=1)
    city: constr(min_length=1)
    postal_code: Annotated[str, Field(alias="postalCode")]

    @field_validator("postal_code")
    @classmethod
    def postal_code_normalize(cls, v: str) -> str:
        return v.strip().upper()
    