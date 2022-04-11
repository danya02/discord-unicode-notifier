from discord.ext import commands
import discord
import os

from cogs import inspect, normalize, lookup, details, new_character_warning

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='&')
bot.add_cog(inspect.Inspect(bot))
bot.add_cog(normalize.Normalize(bot))
bot.add_cog(lookup.Lookup(bot))
bot.add_cog(details.Details(bot))
new_char_warn = new_character_warning.NewCharacterWarning(bot)
bot.add_cog(new_char_warn)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(activity=discord.Game(name='&help'))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    ctx = await bot.get_context(message)
    if ctx.command is None:  # If this message is not a command, run the new character warning.
        await new_char_warn.on_message(message)
    
    await bot.invoke(ctx)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # If the command was not found, then we did not respond to the message, 
        # so we can safely check for the new character warning.
        await new_char_warn.on_message(ctx.message)
        return
    await ctx.send(f'An error occurred: {error}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)