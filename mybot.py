import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from datetime import datetime
import random
from random import choice
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

status = ['Ballin', 'Met je gevoelens', 'Huilen']


@bot.event
async def on_ready():
    change_status.start()
    print('Bot is online!')
    print('---------------------')

    @bot.command(name='rules')
    async def rules(member):
        channel = discord.utils.get(member.guild.channels, name='rules')
        embed = discord.Embed(color=0xf5e66f)
        embed.add_field(name="Regels", value="de regels zijn simpel.", inline=False)
        embed.add_field(name="‏‏‎ ‎", value="→ Geen oorlogs misdaden verrichten.", inline=False)
        embed.add_field(name="‏‏‎ ‎", value="→ Gebruik de kanalen alleen voor hun taak en niet voor andere dingen",
                        inline=False)
        embed.add_field(name="‏‏‎ ‎", value="→ Cyberpesten is toegestaan", inline=False)
        embed.add_field(name="‏‏‎ ‎", value="→ Niet spammen lol", inline=False)
        embed.set_image(url='https://media.giphy.com/media/j0kP7fOkKQlYsXTO2r/giphy.gif')
        embed.set_footer(text="reageer met een geel hartje op dit bericht om toegelaten te worden")
        await channel.send(embed=embed)

        # --------------------------------Regels command--------------------------------------------------------

    @bot.event
    async def on_raw_reaction_add(payload):
        message_id = payload.message_id
        if message_id == 853336175447506974:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

            role = None
            if payload.emoji.name == '💛':
                role = discord.utils.get(guild.roles, name='Certified MulaBGaming Member')

            if role is not None:
                member = payload.member
                if member is not None:
                    await member.add_roles(role)
                    print("Alles is gelukt")
                else:
                    print("Serverlid niet gevonden")

            else:
                print("Rol bestaat niet")

    @bot.event
    async def on_raw_reaction_remove(payload):
        message_id = payload.message_id

        if message_id == 853336175447506974:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

            if payload.emoji.name == '💛':
                role = discord.utils.get(guild.roles, name='Certified MulaBGaming Member')

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print("Alles is gelukt")
                else:
                    print("Serverlid niet gevonden")
            else:
                print("Rol niet gevonden")

                # ----------------------rollen geven(werkt) en verwijderen(werkt nu ook)---------------------

    determine_flip = [1, 0]

    @bot.command(name='flip')
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

            # ------------------------------kop of munt------------------------------------------------

    eightball_antwoorden = ["It is certain", "It is decidedly so", "Without a doubt", 'Yes, definitely',
                            "You may rely on it ", "As I see it, yes ", "Most likely", "Outlook good",
                            "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later",
                            "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                            "Don't count on it", "My reply is no", "My sources say no",
                            "Outlook not so good", "Very doubtful"]

    @bot.command(name='ball', aliases=['8ball', '8b'])
    async def magic_8ball(ctx):

        await ctx.send(f"{ctx.author.mention} {random.choice(eightball_antwoorden)} ")

        # --------------------------------magic 8ball-------------------------------------------------

    @bot.command(name='pfp', aliases=['icon', 'p', 'pf'])
    async def pfp(ctx, *, Member: discord.Member = None):
        if not Member:
            embed = discord.Embed(color=0xfcd743)
            embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            userAvatar = Member.avatar_url
            embed = discord.Embed(color=0xfcd743)
            embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
            embed.set_image(url=userAvatar)
            await ctx.send(embed=embed)

            # -----------------------------stuurt de pfp van de author of een member------------------------------------

            @bot.event
            async def on_member_join(member):
                channel = discord.utils.get(member.guild.channels, name='announcements')
                await channel.send(f'Yow {member.mention} welkom in de server')

    @bot.event
    async def on_member_remove(member):
        channel = discord.utils.get(member.guild.channels, name='announcements')
        await channel.send(f'Ik heb je toch niet nodig voor de HAVO {member.mention}')

        # -------------------welkom en goodbye tot ziens------------------------------------------------

        # -------------------------het leaven van de voice channel-----------------------------------------------

    # ------------------------------------level system---------------------------------------------------------------

    # ---------------------------------------afk functie------------------------------------------------------------


@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Game(choice(status)))

    # -----------------------------------------random status ---------------------------------------------------


bot.run(TOKEN)
