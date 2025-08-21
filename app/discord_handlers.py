import discord
from discord import app_commands
from persistence.base import SessionLocal, engine, Base
from services.task_service import TaskService
from domain.models import Priority, Status
from app.embeds import task_embed
from app.views import StatusButtons


class BotClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.none()
        intents.guilds = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


client = BotClient()


@client.event
async def on_ready():
    Base.metadata.create_all(bind=engine)
    print(f"Logged in as {client.user}")


@client.tree.command(name="task_add", description="Create a new task")
@app_commands.describe(
    title="Short title", priority="low|medium|high", description="Optional details"
)
async def task_add(
    interaction: discord.Interaction,
    title: str,
    priority: str = "medium",
    description: str = "",
):
    await interaction.response.defer(ephemeral=True)
    db = SessionLocal()
    svc = TaskService(db)
    t = svc.create_task(
        str(interaction.guild_id),
        str(interaction.channel_id),
        title,
        description,
        Priority(priority),
        interaction.user.id,
        None,
    )
    embed = task_embed(t)

    async def on_change(i: discord.Interaction, status: Status):
        svc.update_status(t.id, status)
        await i.response.edit_message(embed=task_embed(svc.tasks.get(t.id)))

    view = StatusButtons(on_change)
    await interaction.followup.send(
        content="Task created:", embed=embed, view=view, ephemeral=False
    )


@client.tree.command(name="task_list", description="List tasks in this channel")
async def task_list(interaction: discord.Interaction):
    db = SessionLocal()
    svc = TaskService(db)
    tasks = svc.list_tasks(str(interaction.guild_id), str(interaction.channel_id))
    if not tasks:
        await interaction.response.send_message(
            "No tasks yet. Use `/task_add`.", ephemeral=True
        )
        return
    # paginate simple
    text = "\n".join(
        [
            f"**#{t.id}** [{t.priority.value.title()}] {t.title} — {t.status.value.replace('_',' ').title()} "
            + (f"(→ <@{t.assignee_id}>)" if t.assignee_id else "")
            for t in tasks[:25]
        ]
    )
    await interaction.response.send_message(text, ephemeral=True)


@client.tree.command(name="task_update", description="Update a task's status")
@app_commands.describe(
    task_id="Task number", status="not_started|in_progress|blocked|done"
)
async def task_update(interaction: discord.Interaction, task_id: int, status: str):
    db = SessionLocal()
    svc = TaskService(db)
    t = svc.update_status(task_id, Status(status))
    await interaction.response.send_message(embed=task_embed(t), ephemeral=False)


@client.tree.command(name="task_assign", description="Assign task to a user")
async def task_assign(
    interaction: discord.Interaction, task_id: int, user: discord.Member
):
    db = SessionLocal()
    svc = TaskService(db)
    t = svc.assign(task_id, user.id)
    await interaction.response.send_message(
        f"Assigned **#{t.id}** to {user.mention}", ephemeral=False
    )


@client.tree.command(name="task_delete", description="Delete a task")
async def task_delete(interaction: discord.Interaction, task_id: int):
    db = SessionLocal()
    svc = TaskService(db)
    ok = svc.delete(task_id)
    await interaction.response.send_message(
        "Deleted." if ok else "Not found.", ephemeral=True
    )
