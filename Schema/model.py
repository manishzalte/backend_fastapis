from concel_data.database import Base
from sqlalchemy import Column, Integer,String,Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import(DeclarativeBase, Session, mapped_column, Mapped,relationship)

class Posts(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String,nullable=False)
    content : Mapped[str] = mapped_column(String, nullable=False)
    publish : Mapped[bool] = mapped_column(Boolean, server_default='TRUE', nullable= False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone= True),nullable=False, server_default=text('now()'))
    owner_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="posts")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable= False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone= True),nullable=False, server_default=text('now()'))
    posts = relationship("Posts", back_populates="owner", cascade="all, delete")

class Vote(Base):
    __tablename__ = "votes"
    post_id : Mapped[int] = mapped_column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True,nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True,nullable=False)
