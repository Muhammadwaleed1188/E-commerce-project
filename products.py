from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product, User
from ..schemas import product_create, Product_response
from ..auth import get_current_user


router = APIRouter(prefix="/products")


# ==========================================
# CREATE PRODUCT
# ==========================================

@router.post("/", response_model=Product_response)
def create_product(
    data: product_create,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_product = Product(
        product_name=data.product_name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        category=data.category,

        # Automatically assign logged-in user
        user_id=current_user.user_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# ==========================================
# GET ALL PRODUCTS OF LOGGED-IN USER
# ==========================================

@router.get("/my-products", response_model=list[Product_response])
def get_my_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = db.query(Product).filter(
        Product.user_id == current_user.user_id
    ).all()

    return products


# ==========================================
# GET ONE PRODUCT OF LOGGED-IN USER BY ID
# ==========================================

@router.get("/{product_id}", response_model=Product_response)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.user_id == current_user.user_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# ==========================================
# UPDATE PRODUCT
# ==========================================

@router.put("/{product_id}", response_model=Product_response)
def update_product(
    product_id: int,
    data: product_create,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.user_id == current_user.user_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.product_name = data.product_name
    product.description = data.description
    product.price = data.price
    product.stock = data.stock
    product.category = data.category

    db.commit()
    db.refresh(product)

    return product


# ==========================================
# DELETE PRODUCT
# ==========================================

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.user_id == current_user.user_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }