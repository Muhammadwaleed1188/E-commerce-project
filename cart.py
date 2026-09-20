from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Cart, User, Product
from ..schemas import Cart_create, Cart_response, CartUpdate
from ..auth import get_current_user


router = APIRouter(prefix="/cart")


# ==========================================
# ADD PRODUCT TO CART
# ==========================================

@router.post("/", response_model=Cart_response)
def create_cart(
    data: Cart_create,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Check if product exists
    product = db.query(Product).filter(
        Product.product_id == data.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    new_cart = Cart(
        user_id=current_user.user_id,
        product_id=data.product_id,
        quantity=data.quantity
    )

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return new_cart


# ==========================================
# GET LOGGED-IN USER'S CART
# ==========================================

@router.get("/", response_model=list[Cart_response])
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart_items = db.query(Cart).filter(
        Cart.user_id == current_user.user_id
    ).all()

    return cart_items


# ==========================================
# UPDATE CART QUANTITY
# ==========================================

@router.put("/{cart_id}", response_model=Cart_response)
def update_cart(
    cart_id: int,
    data: CartUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart_item = db.query(Cart).filter(
        Cart.cart_id == cart_id,
        Cart.user_id == current_user.user_id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    cart_item.quantity = data.quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item


# ==========================================
# DELETE CART ITEM
# ==========================================

@router.delete("/{cart_id}")
def delete_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart_item = db.query(Cart).filter(
        Cart.cart_id == cart_id,
        Cart.user_id == current_user.user_id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(cart_item)
    db.commit()

    return {
        "message": "Product removed from cart"
    }