from pydantic import BaseModel, EmailStr, field_validator


# =========================
# USER SCHEMAS
# =========================

class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str
    user_address: str
    is_address: bool
    phone_number: str


class User_Response(BaseModel):
    user_name: str
    user_email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    user_email: EmailStr
    user_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================
# PRODUCT SCHEMAS
# =========================

class product_create(BaseModel):
    product_name: str
    description: str
    price: float
    stock: int
    category: str

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        allowed = [
            "electronics",
            "clothing",
            "books",
            "shoes"
        ]

        if value not in allowed:
            raise ValueError("Invalid category")

        return value


class Product_response(BaseModel):
    product_id: int
    product_name: str
    description: str
    price: float
    stock: int
    category: str

    class Config:
        from_attributes = True


# =========================
# CART SCHEMAS
# =========================

class Cart_create(BaseModel):
    product_id: int
    quantity: int


class Cart_response(BaseModel):
    cart_id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartUpdate(BaseModel):
    quantity: int