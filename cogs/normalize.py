from discord.ext import commands
import discord
import unicodedata2

async def generic_normalize(ctx, form, text):
    normalized = unicodedata2.normalize(form, text)
    if normalized == text:
        await ctx.reply(f'Your {len(text)}-character string is already in Normal Form {form[2:]}.', mention_author=False)
        return

    msg = await ctx.reply(f"Your {len(text)}-character string has been put into Normal Form {form[2:]} with length {len(normalized)}:", mention_author=False)
    await msg.reply(normalized, mention_author=False)

class Normalize(commands.Cog):
    """Provides commands for normalizing text."""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='normalize')
    async def normalize(self, ctx):
        """Normalize text to NFC, NFD, NFKC or NFKD."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
    
    @normalize.command(name='nfc')
    async def normalize_nfc(self, ctx, *, text):
        """Normalize text to NFC."""
        await generic_normalize(ctx, 'NFC', text)
    
    @normalize.command(name='nfd')
    async def normalize_nfd(self, ctx, *, text):
        """Normalize text to NFD."""
        await generic_normalize(ctx, 'NFD', text)

    @normalize.command(name='nfkc')
    async def normalize_nfkc(self, ctx, *, text):
        """Normalize text to NFKC."""
        await generic_normalize(ctx, 'NFKC', text)
    
    @normalize.command(name='nfkd')
    async def normalize_nfkd(self, ctx, *, text):
        """Normalize text to NFKD."""
        await generic_normalize(ctx, 'NFKD', text)
