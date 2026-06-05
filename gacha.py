import discord
from discord.ext import commands
import random

# Fruits with rarity chances
FRUITS = {
    "Common": ["Spin Fruit", "Chop Fruit", "Spring Fruit"],
    "Uncommon": ["Bomb Fruit", "Smoke Fruit"],
    "Rare": ["Light Fruit", "Ice Fruit"],
    "Legendary": ["Flame Fruit", "Quake Fruit"],
    "Mythical": ["Dragon Fruit", "Dough Fruit"]
}

RARITY_WEIGHTS = [
    ("Common", 60),
    ("Uncommon", 20),
    ("Rare", 10),
    ("Legendary", 7),
    ("Mythical", 3)
]

# inventory storage
inventory = {}

def get_inventory(user_id):
    if user_id not in inventory:
        inventory[user_id] = []
    return inventory[user_id]


class GachaSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🎰 spin command
    @discord.app_commands.command(name="spin", description="Spin for a fruit")
    async def spin(self, interaction: discord.Interaction):
        roll = random.randint(1, 100)
        cumulative = 0
        rarity = "Common"

        for r, chance in RARITY_WEIGHTS:
            cumulative += chance
            if roll <= cumulative:
                rarity = r
                break

        fruit = random.choice(FRUITS[rarity])

        inv = get_inventory(interaction.user.id)
        inv.append(fruit)

        await interaction.response.send_message(
            f"🎰 You got **{fruit}** ({rarity})!"
        )

    # 📦 inventory
    @discord.app_commands.command(name="inventory", description="Check your fruits")
    async def inventory_cmd(self, interaction: discord.Interaction):
        inv = get_inventory(interaction.user.id)

        if not inv:
            await interaction.response.send_message("📦 You have no fruits yet!")
            return

        await interaction.response.send_message(
            "📦 Your Fruits:\n" + "\n".join(f"- {i}" for i in inv)
        )

    # 💰 sell fruit
    @discord.app_commands.command(name="sell", description="Sell a fruit for money")
    async def sell(self, interaction: discord.Interaction, fruit: str):
        inv = get_inventory(interaction.user.id)

        if fruit not in inv:
            await interaction.response.send_message("❌ You don't own this fruit!")
            return

        inv.remove(fruit)

        # simple pricing system
        price = random.randint(100, 1000)

        await interaction.response.send_message(
            f"💰 Sold **{fruit}** for **{price} coins**!"
        )


async def setup(bot):
    await bot.add_cog(GachaSystem(bot))
