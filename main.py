from discord.ext import commands
import discord
import os

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='&help'))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
