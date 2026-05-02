from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    store = Column(String)
    rfc = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    folio = Column(String, nullable=True)
    date = Column(String)
    time = Column(String, nullable=True)
    total = Column(Float)
    currency = Column(String, default="MXN")
    macro = Column(String)
    subcategory = Column(String)
    confidence_score = Column(Float)
    registered_at = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class StoreRule(Base):
    __tablename__ = "store_rules"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, unique=True, index=True)
    macro = Column(String)
    subcategory = Column(String)
    confidence_score = Column(Float, default=0.95)
    created_at = Column(DateTime, default=datetime.now)


class Exception(Base):
    __tablename__ = "exceptions"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, index=True)
    user_id = Column(String)
    macro = Column(String)
    subcategory = Column(String)
    created_at = Column(DateTime, default=datetime.now)
