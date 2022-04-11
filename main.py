from discord.ext import commands
import discord
import os

from cogs import inspect, normalize, lookup

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='&')
bot.add_cog(inspect.Inspect(bot))
bot.add_cog(normalize.Normalize(bot))
bot.add_cog(lookup.Lookup(bot))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='&help'))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)