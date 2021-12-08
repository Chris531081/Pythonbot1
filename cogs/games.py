import discord
from discord.ext import commands
import random


class Games(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

        determine_flip = [1, 0]

        @commands.command(name='flip')
        async def coinflip(ctx):
            if random.choice(determine_flip) == 1:
                embed = discord.Embed(title="Kop of Munt",
                                      description=f"{ctx.author.mention} De munt is geflipped je hebt **Kop**!",
                                      color=0xfcd743)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="Kop of Munt",
                                      description=f"{ctx.author.mention} De munt is geflipped je hebt **Munt**!",
                                      color=0xfcd743)
                await ctx.send(embed=embed)
