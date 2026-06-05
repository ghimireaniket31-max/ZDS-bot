import discord
from discord.ext import commands
import random
import time

# Simple in-memory database (you can later switch to SQLite)
user_data = {}

def get_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "xp": 0,
            "level": 1,
            "last_message": 0
        }
    return user_data[user_id]


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # XP system
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user = get_user(message.author.id)

        # cooldown (prevents spam XP farming)
        now = time.time()
        if now - user["last_message"] < 5:
            return

        user["last_message"] = now

        # random XP gain
        xp_gain = random.randint(5, 15)
        user["xp"] += xp_gain

        # level up system
        xp_needed = user["level"] * 100

        if user["xp"] >= xp_needed:
            user["xp"] -= xp_needed
            user["level"] += 1

            await message.channel.send(
                f"🔥 {message.author.mention} leveled up to **Level {user['level']}**!"
            )

    # check level command
    @discord.app_commands.command(name="level", description="Check your level")
    async def level(self, interaction: discord.Interaction):
        user = get_user(interaction.user.id)

        await interaction.response.send_message(
            f"📊 {interaction.user.mention}\n"
            f"Level: **{user['level']}**\n"
            f"XP: **{user['xp']} / {user['level'] * 100}**"
        )


async def setup(bot):
    await bot.add_cog(LevelSystem(bot))
