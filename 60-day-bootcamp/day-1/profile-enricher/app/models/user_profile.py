from pydantic import BaseModel, Field, field_validator, model_validator, conint, constr
from typing import Optional, Dict, Any
from app.models.address import Address

class UserProfile(BaseModel):
    user_id: constr(min_length=1) = Field(..., alias="userId")
    username: constr(min_length=3, max_length=32) = Field(..., alias="username")
    email: constr(min_length=5)  # will run validator
    age: Optional[conint(gt=0, lt=130)] = None
    address: Optional[Address] = None
    signup_ts: Optional[str] = Field(None, alias="signupTs")

    # Example field validator: normalize email
    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    # Cross-field validation example
    @model_validator(mode="after")
    def check_username_vs_email(self) -> "UserProfile":
        # Ensure username not equal to email local part (toy rule)
        local_part = self.email.split("@")[0] if "@" in self.email else ""
        print(f"local_part: {local_part}")
        if local_part and local_part == self.username:
            raise ValueError("username must not equal email local-part for security reasons")
        return self

    def to_public_dict(self) -> Dict[str, Any]:
        # Controlled serialization
        return self.model_dump(by_alias=True, exclude_none=True)