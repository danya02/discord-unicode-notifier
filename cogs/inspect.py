from discord.ext import commands
import discord
import unicodedata2
import utils

def inspect_text(text):
    output = f'I received the following {len(text)} characters:\n'
    for char in text:
        output += utils.char_description(char) + '\n'
    return output

class Inspect(commands.Cog):
    """Provides commands for inspecting the contents of a text line."""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='version')
    async def version(self, ctx):
        """Return the version of the Unicode table being used."""
        await ctx.reply(f'Using Unicode table v{unicodedata2.unidata_version}', mention_author=False)

    @commands.cooldown(2, 15, commands.BucketType.guild)
    @commands.command(name='inspect')
    async def inspect(self, ctx, *, text):
        """Show characters in text in single message."""
        output = inspect_text(text)
        output = output.split('\n')
        # If this does not fit in a single message, discard lines until it does.
        truncated_lines = 0
        while len('\n'.join(output)) > 1950:  # Discord's max message length is 2000, and leaving some margin for the final line.
            output.pop()
            truncated_lines += 1
        
        if truncated_lines > 0:
            output.append(f'... and {truncated_lines} more characters.')

        await ctx.reply('\n'.join(output), mention_author=False)


    @commands.command(name='inspect-full')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def inspect_full(self, ctx, *, text: str):
        """Show characters in text in multiple messages."""
        output = inspect_text(text)

        # The output might be too long to fit in a single message.
        # So we split it into multiple messages.

        message = None
        for content in utils.split_into_messages(output):
            if message:
                message = await message.reply(content, mention_author=False)
            else:
                message = await ctx.reply(content, mention_author=False)

    async def cog_command_error(self, ctx, error):
        await ctx.reply(str(error))
