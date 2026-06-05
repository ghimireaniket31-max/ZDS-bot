import discord
from discord.ext import commands
import json
import os

MAX_CREDITS = 1_000_000_000_000

class Economy(commands.Cog):
def init(self, bot):
self.bot = bot
self.file = "users.json"

    if not os.path.exists(self.file):
        with open(self.file, "w") as f:
            json.dump({}, f)

def load_data(self):
    with open(self.file, "r") as f:
        return json.load(f)

def save_data(self, data):
    with open(self.file, "w") as f:
        json.dump(data, f, indent=4)

@commands.hybrid_command(name="balance")
async def balance(self, ctx, member: discord.Member = None):
    member = member or ctx.author

    data = self.load_data()

    if str(member.id) not in data:
        data[str(member.id)] = {"credits": 0}
        self.save_data(data)

    await ctx.send(
        f"💰 {member.display_name} has {data[str(member.id)]['credits']:,} credits."
    )

@commands.hybrid_command(name="addcredits")
@commands.has_permissions(manage_guild=True)
async def addcredits(self, ctx, member: discord.Member, amount: int):

    data = self.load_data()

    if str(member.id) not in data:
        data[str(member.id)] = {"credits": 0}

    data[str(member.id)]["credits"] += amount

    if data[str(member.id)]["credits"] > MAX_CREDITS:
        data[str(member.id)]["credits"] = MAX_CREDITS

    self.save_data(data)

    await ctx.send(
        f"✅ Added {amount:,} credits to {member.mention}"
    )

@commands.hybrid_command(name="removecredits")
@commands.has_permissions(manage_guild=True)
async def removecredits(self, ctx, member: discord.Member, amount: int):

    data = self.load_data()

    if str(member.id) not in data:
        data[str(member.id)] = {"credits": 0}

    data[str(member.id)]["credits"] -= amount

    if data[str(member.id)]["credits"] < 0:
        data[str(member.id)]["credits"] = 0

    self.save_data(data)

    await ctx.send(
        f"❌ Removed {amount:,} credits from {member.mention}"
    )

async def setup(bot):
await bot.add_cog(Economy(bot))
