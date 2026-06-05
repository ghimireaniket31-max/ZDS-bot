import discord
from discord.ext import commands
import json
import os
import random

class Levels(commands.Cog):
def init(self, bot):
self.bot = bot
self.file = "levels.json"

    if not os.path.exists(self.file):
        with open(self.file, "w") as f:
            json.dump({}, f)

def load_data(self):
    with open(self.file, "r") as f:
        return json.load(f)

def save_data(self, data):
    with open(self.file, "w") as f:
        json.dump(data, f, indent=4)

@commands.Cog.listener()
async def on_message(self, message):
    if message.author.bot:
        return

    data = self.load_data()
    uid = str(message.author.id)

    if uid not in data:
        data[uid] = {
            "xp": 0,
            "level": 1
        }

    xp_gain = random.randint(5, 15)
    data[uid]["xp"] += xp_gain

    level = data[uid]["level"]
    needed = level * 100

    if data[uid]["xp"] >= needed:
        data[uid]["xp"] = 0
        data[uid]["level"] += 1

        await message.channel.send(
            f"🎉 {message.author.mention} reached Level {data[uid]['level']}!"
        )

    self.save_data(data)

@commands.hybrid_command(name="rank")
async def rank(self, ctx, member: discord.Member = None):

    member = member or ctx.author

    data = self.load_data()
    uid = str(member.id)

    if uid not in data:
        data[uid] = {
            "xp": 0,
            "level": 1
        }

    await ctx.send(
        f"⭐ {member.display_name}\nLevel: {data[uid]['level']}\nXP: {data[uid]['xp']}"
    )

@commands.hybrid_command(name="leaderboard")
async def leaderboard(self, ctx):

    data = self.load_data()

    sorted_users = sorted(
        data.items(),
        key=lambda x: x[1]["level"],
        reverse=True
    )[:10]

    text = "🏆 Level Leaderboard\n\n"

    for i, (uid, info) in enumerate(sorted_users, start=1):
        text += f"{i}. <@{uid}> - Level {info['level']}\n"

    await ctx.send(text)

async def setup(bot):
await bot.add_cog(Levels(bot))
