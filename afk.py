import discord
from discord.ext import commands

afk_users = {}

class AFK(commands.Cog):
def init(self, bot):
self.bot = bot

@commands.hybrid_command(name="afk")
async def afk(self, ctx, *, reason="AFK"):
    afk_users[ctx.author.id] = reason
    await ctx.send(f"💤 {ctx.author.mention} is now AFK: {reason}")

@commands.Cog.listener()
async def on_message(self, message):

    if message.author.bot:
        return

    if message.author.id in afk_users:
        del afk_users[message.author.id]
        await message.channel.send(
            f"👋 Welcome back {message.author.mention}, AFK removed."
        )

    for user in message.mentions:
        if user.id in afk_users:
            await message.channel.send(
                f"💤 {user.display_name} is AFK: {afk_users[user.id]}"
            )

async def setup(bot):
await bot.add_cog(AFK(bot))
