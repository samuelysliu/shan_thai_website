from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from Modules.dbConnect import engine, Base

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

class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(String)
    content_en = Column(String)
    aboutImageUrl = Column(String)
    
class Product(Base):
    __tablename__ = "product"

    pid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_cn = Column(String(255), index=True)
    title_en = Column(String(255))
    content_cn = Column(String)
    content_en = Column(String)
    price = Column(Integer, default=0)
    specialPrice = Column(Integer, default=None, nullable=True)
    remain = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    productImageUrl = Column(String)
    
class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_cn = Column(String(255), index=True)
    name_en = Column(String(255))
    title_cn = Column(String(255))
    title_en = Column(String(255))
    teamImageUrl = Column(String)
    
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
    
class ExternalLink(Base):
    __tablename__ = "external_link"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_cn = Column(String(255), index=True)
    name_en = Column(String(255))
    iconImageUrl = Column(String)
    show = Column(Boolean)

class User(Base):
    __tablename__ = "users"
    uid = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    sex = Column(String(255), nullable=True)
    star = Column(Integer, default=0)
    identity = Column(String(255), nullable=True)
    note = Column(String(255), nullable=True)
    
class Order(Base):
    __tablename__ = "orders"
    oid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)
    pid = Column(Integer, ForeignKey("product.pid"), nullable=False)
    productNumber = Column(Integer, default=1)
    address = Column(String)
    transportationMethod = Column(String(50))
    status = Column(String(50))

Base.metadata.create_all(bind=engine)