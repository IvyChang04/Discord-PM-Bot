from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base
from domain.models import Status, Priority


def utcnow():
    return datetime.now(tz=timezone.utc)


class ProjectORM(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    guild_id = Column(String, index=True, nullable=False)
    channel_id = Column(String, index=True, nullable=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)


class TaskORM(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    status = Column(SAEnum(Status), default=Status.NOT_STARTED, nullable=False)
    priority = Column(SAEnum(Priority), default=Priority.MEDIUM, nullable=False)
    creator_id = Column(String, nullable=False)
    assignee_id = Column(String, nullable=True)
    due_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
