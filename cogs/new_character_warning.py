import aiohttp
from discord.ext import commands
import discord
import unicodedata2
import utils

# Ages of the Unicode standard to warn about.
NEW_AGES = ['14.0']

class NewCharacterWarning(commands.Cog):
    """Warns about new characters."""

    def __init__(self, bot):
        self.bot = bot
        self.age_chars = None

    async def get_char_age(self):
        """Get the age of all characters."""
        if self.age_chars is not None:
            return self.age_chars

        self.age_chars = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.unicode.org/Public/{unicodedata2.unidata_version}/ucd/DerivedAge.txt') as request:
                for line in (await request.text()).splitlines():
                    line = line.split('#')[0].strip()
                    if not line:
                        continue
                    code, age = line.split(';')
                    code = code.strip()
                    age = age.strip()
                    if '..' in code:
                        start, end = code.split('..')
                        start = int(start, 16)
                        end = int(end, 16)
                        code = range(start, end + 1)
                    else:
                        code = int(code, 16)
                    self.age_chars[age] = self.age_chars.get(age, []) + [code]
        
        for age in self.age_chars:
            self.age_chars[age] = set(self.age_chars[age])

        return self.age_chars


    #@commands.Cog.listener()
    # This should only be run if the message did not end up running a command.
    # So we will run this manually from main.py.
    async def on_message(self, message):
        if message.author.bot:
            return
        content = message.content or ''

        age_chars = await self.get_char_age()

        warning_chars = []
        # Check if the message contains a character that is new.
        for char in content:
            char = ord(char)
            for age in NEW_AGES:
                for aged_char in age_chars.get(age, []):
                    if isinstance(aged_char, int):
                        if char == aged_char:
                            warning_chars.append(char)
                    else:
                        if char in aged_char:
                            warning_chars.append(char)
        
        shown_warning_chars = set()
        if warning_chars:
            description = f"Some characters in this message are from a new version of Unicode, so they might render incorrectly:\n"
            for char in warning_chars:
                char = chr(char)
                if char in shown_warning_chars: continue
                description += utils.char_description(char) + '\n'
                shown_warning_chars.add(char)
        
        await message.reply(utils.truncate_to_message(description)[0], mention_author=False)