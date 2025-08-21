from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


class Status(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    id: int
    project_id: int
    title: str
    description: str
    status: Status
    priority: Priority
    creator_id: int
    assignee_id: Optional[int]
    due_at: Optional[datetime]
    create_at: datetime
    updated_at: datetime


def utcnow():
    return datetime.now(tz=timezone.utc)
