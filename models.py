from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv()
engine = create_engine(f'{ os.environ.get("DATABASE_URL")}'.replace('postgres://', 'postgresql://'))
Base = declarative_base()
metadata = Base.metadata

class TelegramUser(Base):
    __tablename__ = 'telegram_user'

    id = Column(Integer, primary_key=True)
    first_start_timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    is_stopped = Column(Integer, default=0)
    first_name = Column(String)
    last_name = Column(String)

    def __repr__(self):
        return f'TelegramUser(id={self.id}, first_name={self.first_name}, last_name={self.last_name})'