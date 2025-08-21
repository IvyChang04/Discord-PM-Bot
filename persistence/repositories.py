from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import TaskORM, ProjectORM
from domain.models import Status, Priority


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **data) -> TaskORM:
        task = TaskORM(**data)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get(self, task_id: int) -> Optional[TaskORM]:
        return self.db.get(TaskORM, task_id)

    def list(self, project_id: int) -> List[TaskORM]:
        return list(
            self.db.execute(
                select(TaskORM).where(TaskORM.project_id == project_id)
            ).scalars()
        )

    def save(self, task: TaskORM) -> TaskORM:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(
        self, guild_id: str, channel_id: Optional[str], name: str = "default"
    ) -> ProjectORM:
        q = select(ProjectORM).where(
            ProjectORM.guild_id == guild_id,
            ProjectORM.channel_id == channel_id,
            ProjectORM.name == name,
        )
        p = self.db.execute(q).scalar_one_or_none()
        if p:
            return p
        p = ProjectORM(guild_id=guild_id, channel_id=channel_id, name=name)
        self.db.add(p)
        self.db.commit()
        self.db.refresh(p)
        return p
