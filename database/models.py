from database.connection import Base, engine

from sqlalchemy import Column, Integer, Date, String, BigInteger, DECIMAL, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class ImportedData(Base):
    __tablename__ = "imported_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    random_date = Column(Date, nullable=True)
    latin_string = Column(String(100), nullable=True)
    russian_string = Column(String(100), nullable=True)
    even_integer = Column(BigInteger, nullable=True)
    float_number = Column(DECIMAL(12, 8), nullable=True)
    file_name = Column(Text, nullable=True)
    imported_at = Column(DateTime, server_default=func.now(), nullable=False)


Base.metadata.create_all(engine)
