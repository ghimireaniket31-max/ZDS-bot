import discord
from discord import app_commands
from discord.ext import commands
import time

# Simple in-memory warn storage (reset when bot restarts)
warnings = {}

# Basic bad words list (edit this)
BAD_WORDS = ["badword1", "badword2", "fuck", "shit"]

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------------- AUTO MODERATION ----------------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        content = message.content.lower()

        for word in BAD_WORDS:
            if word in content:
                try:
                    await message.delete()
                    await message.channel.send(
                        f"🚫 {message.author.mention}, that language is not allowed!",
                        delete_after=5
                    )
                except:
                    pass
                break

    # ---------------- KICK ----------------
    @app_commands.command(name="kick", description="Kick a member")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 {member} has been kicked. Reason: {reason}")

    # ---------------- BAN ----------------
    @app_commands.command(name="ban", description="Ban a member")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member} has been banned. Reason: {reason}")

    # ---------------- TIMEOUT ----------------
    @app_commands.command(name="timeout", description="Timeout a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason provided"):
        duration = discord.utils.utcnow() + discord.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)

        await interaction.response.send_message(
            f"⏳ {member} has been timed out for {minutes} minutes. Reason: {reason}"
        )

    # ---------------- WARN ----------------
    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        user_id = member.id

        if user_id not in warnings:
            warnings[user_id] = []

        warnings[user_id].append({
            "reason": reason,
            "moderator": interaction.user.name,
            "time": int(time.time())
        })

        await interaction.response.send_message(
            f"⚠️ {member} has been warned. Reason: {reason}"
        )

    # ---------------- CHECK WARNINGS ----------------
    @app_commands.command(name="warnings", description="Check warnings of a user")
    async def warnings_cmd(self, interaction: discord.Interaction, member: discord.Member):
        user_warnings = warnings.get(member.id, [])

        if not user_warnings:
            await interaction.response.send_message(f"✅ {member} has no warnings.")
            return

        msg = f"⚠️ Warnings for {member}:\n"
        for i, w in enumerate(user_warnings, 1):
            msg += f"{i}. {w['reason']} (by {w['moderator']})\n"

        await interaction.response.send_message(msg)

    # ---------------- CLEAR MESSAGES ----------------
    @app_commands.command(name="clear", description="Delete messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"🧹 Deleted {amount} messages.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
