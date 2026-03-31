from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class Status(enum.Enum):
    IN_STOCK = "На складе"
    IN_SERVICE = "В сервисе"
    READY = "Готов"
    ASSIGNED = "Выдан"

class Cartridge(Base):
    __tablename__ = "cartridges"

    id = Column(Integer, primary_key=True)
    model = Column(String)
    owner = Column(String, nullable=True)
    status = Column(Enum(Status), default=Status.IN_STOCK)


class CartridgeLog(Base):
    __tablename__ = "cartridge_logs"

    id = Column(Integer, primary_key=True)
    cartridge_id = Column(Integer, ForeignKey("cartridges.id"))
    action = Column(String)
    user = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
