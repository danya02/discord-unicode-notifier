from discord.ext import commands
import discord
import unicodedata2
import utils

class Lookup(commands.Cog):
    """Find characters by name."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='lookup')
    async def lookup(self, ctx, *, text):
        """Look up a character by its Unicode name."""
        try:
            character = unicodedata2.lookup(text)
        except KeyError:
            await ctx.reply(f'No character named `{text}` found.', mention_author=False)
            return
        await ctx.reply(utils.char_description(character), mention_author=False)