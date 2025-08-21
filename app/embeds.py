import discord
from domain.models import Status, Priority


def task_embed(task) -> discord.Embed:
    e = discord.Embed(
        title=f"#{task.id} • {task.title}",
        description=task.description or "",
        timestamp=task.updated_at,
    )
    e.add_field(name="Status", value=task.status.value.replace("_", " ").title())
    e.add_field(name="Priority", value=task.priority.value.title())
    e.add_field(
        name="Assignee", value=f"<@{task.assignee_id}>" if task.assignee_id else "—"
    )
    return e
