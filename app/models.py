from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(server_default='TRUE' , nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 server_default=text('NOW()'))
    # created_at = Column(TIMESTAMP(timezone=True), 
    #                     nullable=False, server_default=text('NOW()'))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="posts")


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, 
                                                 server_default=text('NOW()'))
    posts: Mapped[list[Post]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class Vote(Base):
    __tablename__ = "votes"
    
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    __table_args__ = (
        PrimaryKeyConstraint("post_id", "user_id"),
    )

def model_to_dict(model):
    return {
        column.key: getattr(model, column.key)
        for column in inspect(model).mapper.column_attrs
    }