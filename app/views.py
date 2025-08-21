import discord
from domain.models import Status


class StatusButtons(discord.ui.View):
    def __init__(self, on_change, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.on_change = on_change

    @discord.ui.button(label="Start", style=discord.ButtonStyle.primary)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.on_change(interaction, Status.IN_PROGRESS)

    @discord.ui.button(label="Block", style=discord.ButtonStyle.danger)
    async def block(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.on_change(interaction, Status.BLOCKED)

    @discord.ui.button(label="Done", style=discord.ButtonStyle.success)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.on_change(interaction, Status.DONE)
