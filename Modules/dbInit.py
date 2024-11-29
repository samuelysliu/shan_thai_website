from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from Modules.dbConnect import engine, Base
from sqlalchemy.sql import func

class Banner(Base):
    __tablename__ = "banner"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(String)
    content_en = Column(String)
    buttonText_cn = Column(String(255))
    buttonText_en = Column(String(255))
    buttonLink = Column(String)
    bannerImageUrl = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(Text)
    content_en = Column(Text)
    aboutImageUrl = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_cn = Column(String(255), index=True)
    name_en = Column(String(255))
    title_cn = Column(String(255))
    title_en = Column(String(255))
    teamImageUrl = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(String)
    content_en = Column(String)
    address_cn = Column(String(255))
    address_en = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
class ExternalLink(Base):
    __tablename__ = "external_link"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_cn = Column(String(255), index=True)
    name_en = Column(String(255))
    iconImageUrl = Column(String)
    show = Column(Boolean)
    externalLink = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Product(Base):
    __tablename__ = "product"

    pid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ptid = Column(Integer, ForeignKey("product_tag.ptid"))
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(Text)
    content_en = Column(Text)
    price = Column(Integer, default=0)
    specialPrice = Column(Integer, default=None, nullable=True)
    remain = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    productImageUrl = Column(String)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 關聯其他資料庫
    orders = relationship("Order", back_populates="product")
    carts = relationship("Cart", back_populates="product")
    product_tag = relationship("ProductTag", back_populates="product")
    
class User(Base):
    __tablename__ = "users"
    uid = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    sex = Column(String(255), nullable=True)
    star = Column(Integer, default=0)
    identity = Column(String(255), nullable=True)
    note =Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 關聯其他資料庫
    carts = relationship("Cart", back_populates="users")
    orders = relationship("Order", back_populates="users")

    
class Order(Base):
    __tablename__ = "orders"
    oid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)
    pid = Column(Integer, ForeignKey("product.pid"), nullable=False)
    productNumber = Column(Integer, default=1)
    totalAmount = Column(Integer, default=0)  # 新增欄位：訂單金額
    address = Column(String)
    transportationMethod = Column(String(50))
    status = Column(String(50))
    created_at = Column(DateTime, default=func.now(), onupdate=func.now()) 
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 關聯其他資料庫
    users = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")


class Term(Base):
    __tablename__ = "terms"

    tid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    version = Column(String(50), nullable=False)  # 版本名稱
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Cart(Base):
    __tablename__ = "carts"

    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)
    pid = Column(Integer, ForeignKey("product.pid"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    added_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)  # 是否有效
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 關聯其他資料庫
    users = relationship("User", back_populates="carts")
    product = relationship("Product", back_populates="carts")

class ProductTag(Base):
    __tablename__ = "product_tag"

    ptid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    productTag = Column(String(255), nullable=False)
    
    # 關聯其他資料庫
    product = relationship("Product", back_populates="product_tag")

Base.metadata.create_all(bind=engine)