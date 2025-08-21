from datetime import datetime
from sqlalchemy.orm import Session
from persistence.repositories import ProjectRepository, TaskRepository
from domain.models import Status, Priority


class TaskService:
    def __init__(self, db: Session):
        self.tasks = TaskRepository(db=db)
        self.project = ProjectRepository(db=db)

    def create_task(
        self,
        guild_id: str,
        channel_id: str,
        title: str,
        description: str,
        priority: Priority,
        creator_id: int,
        due_at: datetime | None,
    ):
        project = self.project.get_or_create(guild_id=guild_id, channel_id=channel_id)
        return self.tasks.create(
            project_id=project.id,
            title=title,
            description=description or "",
            priority=priority,
            creator_id=str(creator_id),
        )

    def list_tasks(self, guild_id: str, channel_id: str):
        project = self.project.get_or_create(guild_id=guild_id, channel_id=channel_id)
        return self.tasks.list(project_id=project.id)

    def update_status(self, task_id: int, status: Status):
        task = self.tasks.get(task_id=task_id)
        if not task:
            raise ValueError("Task not found")
        task.status = status
        return self.tasks.save(task=task)

    def assign(self, task_id: int, assignee_id: int | None):
        task = self.tasks.get(task_id=task_id)
        if not task:
            raise ValueError("Task not found")
        task.assignee_id = str(assignee_id) if assignee_id else None
        return self.tasks.save(task=task)

    def delete(self, task_id: int):
        task = self.tasks.get(task_id=task_id)
        from persistence.base import SessionLocal

        self.tasks.db.delete(task)
        self.tasks.db.commit()
        return True
