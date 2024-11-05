from sqlalchemy import Column, Integer, String
from dbConnect import engine, Base

class Banner(Base):
    __tablename__ = "banner"

    id = Column(Integer, primary_key=True, index=True)
    title_cn = Column(String, index=True)
    title_en = Column(String)
    content_cn = Column(String)
    content_en = Column(String)
    buttonText_cn = Column(String)
    buttonText_en = Column(String)
    buttonLink = Column(String)
    bannerImageUrl = Column(String)

class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True)
    title_cn = Column(String, index=True)
    title_en = Column(String)
    content_cn = Column(String)
    content_en = Column(String)
    aboutImageUrl = Column(String)
    
class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    title_cn = Column(String, index=True)
    title_en = Column(String)
    content_cn = Column(String)
    content_en = Column(String)
    productImageUrl = Column(String)
    
class CustomerSay(Base):
    __tablename__ = "customerSay"

    id = Column(Integer, primary_key=True, index=True)
    name_cn = Column(String, index=True)
    name_en = Column(String)
    content_cn = Column(String)
    content_en = Column(String)
    customerImageUrl = Column(String)
    
class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    name_cn = Column(String, index=True)
    name_en = Column(String)
    title_cn = Column(String)
    title_en = Column(String)
    teamImageUrl = Column(String)
    
class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    title_cn = Column(String, index=True)
    title_en = Column(String)
    content_cn = Column(String)
    content_en = Column(String)
    address_cn = Column(String)
    address_en = Column(String)
    phone = Column(String)
    email = Column(String)
    
class ExternalLink(Base):
    __tablename__ = "externalLink"

    id = Column(Integer, primary_key=True, index=True)
    name_cn = Column(String, index=True)
    name_en = Column(String)
    iconImageUrl = Column(String)
    show = Column(Boolean)

Base.metadata.create_all(bind=engine)