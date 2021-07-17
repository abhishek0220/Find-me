from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import RelationshipProperty, relationship
from fastapi_sqlalchemy import db
import uuid
import time

Base = declarative_base()


def get_random_uuid():
    return ''.join(str(uuid.uuid4()).split('-'))


def get_current_time():
    return str(int(time.time()))


task_association_table = Table(
    'task_association_table', Base.metadata,
    Column('user', Integer, ForeignKey('users.id')),
    Column('task', Integer, ForeignKey('tasks.id'))
)


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    display_picture = Column(String, nullable=True)
    score = Column(Integer, default=0)

    tasks_added: RelationshipProperty = relationship("TaskModel", back_populates="author")
    task_completed: RelationshipProperty = relationship(
        "TaskModel",
        secondary=task_association_table,
        back_populates="completed_by"
    )

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)


class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("UserModel", back_populates="tasks_added")
    latitude = Column(String)
    longitude = Column(String)
    title = Column(String)
    image_url = Column(String)
    hints = Column(String)
    description = Column(String)
    city = Column(String)
    time_added = Column(String, default=get_current_time)
    country = Column(String)
    completed_by = relationship(
        "UserModel",
        secondary=task_association_table,
        back_populates="task_completed"
    )

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
