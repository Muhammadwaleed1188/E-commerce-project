from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    user_email = Column(String)
    user_password = Column(String)
    user_address = Column(String)
    is_address = Column(Boolean, default=False)
    phone_number = Column(String)

    # User can have many cart items
    cart_items = relationship("Cart", back_populates="user")

    # User can create many products
    products = relationship("Product", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String)

    # Product belongs to a user
    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="products")

    # Product can be in many cart items
    cart_items = relationship("Cart", back_populates="product")


class Cart(Base):
    __tablename__ = "cart"

    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")