from re import M
from discord.ext import commands
import discord
import unicodedata2
import utils

categories = {  # https://www.unicode.org/reports/tr44/#General_Category_Values
    'Cc': 'Other, Control',
    'Cf': 'Other, Format',
    'Cn': 'Other, Not Assigned',
    'Co': 'Other, Private Use',
    'Cs': 'Other, Surrogate',
    'Ll': 'Letter, Lowercase',
    'Lm': 'Letter, Modifier',
    'Lo': 'Letter, Other',
    'Lt': 'Letter, Titlecase',
    'Lu': 'Letter, Uppercase',
    'Mc': 'Mark, Spacing Combining',
    'Me': 'Mark, Enclosing',
    'Mn': 'Mark, Nonspacing',
    'Nd': 'Number, Decimal Digit',
    'Nl': 'Number, Letter',
    'No': 'Number, Other',
    'Pc': 'Punctuation, Connector',
    'Pd': 'Punctuation, Dash',
    'Pe': 'Punctuation, Close',
    'Pf': 'Punctuation, Final quote',
    'Pi': 'Punctuation, Initial quote',
    'Po': 'Punctuation, Other',
    'Ps': 'Punctuation, Open',
    'Sc': 'Symbol, Currency',
    'Sk': 'Symbol, Modifier',
    'Sm': 'Symbol, Math',
    'So': 'Symbol, Other',
    'Zl': 'Separator, Line',
    'Zp': 'Separator, Paragraph',
    'Zs': 'Separator, Space'
}

bidi_classes = {  # https://www.unicode.org/reports/tr44/#Bidi_Class_Values
    'L': 'Strong Left-to-Right',
    'R': 'Strong Right-to-Left',
    'AL': 'Arabic Letter',
    'EN': 'European Number',
    'ES': 'European Separator',
    'ET': 'European Terminator',
    'AN': 'Arabic Number',
    'CS': 'Common Separator',
    'NSM': 'Nonspacing Mark',
    'BN': 'Boundary Neutral',
    'B': 'Paragraph Separator',
    'S': 'Segment Separator',
    'P': 'Paragraph Separator',
    'WS': 'Whitespace',
    'ON': 'Other Neutrals',
    'LRE': 'Left-to-Right Embedding',
    'LRO': 'Left-to-Right Override',
    'RLE': 'Right-to-Left Embedding',
    'RLO': 'Right-to-Left Override',
    'PDF': 'Pop Directional Format',
    'LRI': 'Left-to-Right Isolate',
    'RLI': 'Right-to-Left Isolate',
    'FSI': 'First Strong Isolate',
    'PDI': 'Pop Directional Isolate'
}

combining_classes = {  # https://www.unicode.org/reports/tr44/#Canonical_Combining_Class_Values
    0: 'Not Reordered',
    1: 'Overlay',
    6: 'Han Reading',
    7: 'Nukta',
    8: 'Kana Voicing',
    9: 'Virama',
    200: 'Attached Below Left',
    202: 'Attached Below',
    204: 'Unnamed [Attached at Bottom Right]',
    208: 'Unnamed [Attached to Left]',
    210: 'Unnamed [Attached to Right]',
    212: 'Unnamed [Attached at Top Left]',
    214: 'Attached Above [Distinct]',
    216: 'Attached Above Right [Distinct]',
    218: 'Below Left [Distinct]',
    220: 'Below [Distinct]',
    222: 'Below Right [Distinct]',
    224: 'Left [Distinct]',
    226: 'Right [Distinct]',
    228: 'Above Left [Distinct]',
    230: 'Above [Distinct]',
    232: 'Above Right [Distinct]',
    233: 'Double Below [Distinct]',
    234: 'Double Above [Distinct]',
    240: 'Iota Subscript',
}

east_asian_width_classes = {  # https://www.unicode.org/reports/tr11/#ED1
    'F': 'Fullwidth',
    'H': 'Halfwidth',
    'W': 'Wide',
    'Na': 'Narrow',
    'A': 'Ambiguous',
    'N': 'Neutral'
}
class Details(commands.Cog):
    """Show details for character."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='details')
    async def details(self, ctx, *, text):
        """Show details for character."""
        character = None

        # Try parsing the character in different ways.
        if len(text) == 1: # Single character.
            character = text
        elif text.startswith('U+'): # U+xxxx
            try:
                character = int(text[2:], 16)
                character = chr(character)
            except ValueError:
                await ctx.reply(f'Invalid character code `{text}`.', mention_author=False)
                return
        else:
            try:
                character = unicodedata2.lookup(text) # Unicode name.
            except KeyError:
                pass
        
        if character is None:
            await ctx.reply(f'Could not figure out which character you meant. You must provide a single character, a `U+xxxx` code, or a Unicode name.', mention_author=False)
            return
        
        description = utils.char_description(character) + '\n'
        try:
            description += f'Decimal value: {unicodedata2.decimal(character)}\n'
        except ValueError:
            description += 'Has no decimal value.\n'
        
        try:
            description += f'Digit value: {unicodedata2.digit(character)}\n'
        except ValueError:
            description += 'Has no digit value.\n'
        
        try:
            description += f'Numeric value: {unicodedata2.numeric(character)}\n'
        except ValueError:
            description += 'Has no numeric value.\n'

        try:
            category = unicodedata2.category(character)
            cat_name = categories.get(category, '[Unknown category name]')
            description += f'Category: {cat_name} ({category})\n'
        except:
            description += 'Unexpected error while getting category.\n'
        
        try:
            bidi_class = unicodedata2.bidirectional(character)
            bidi_name = bidi_classes.get(bidi_class, '[Unknown bidirectional class name]')
            description += f'Bidirectional class: {bidi_name} ({bidi_class})\n'
        except:
            description += 'Unexpected error while getting bidirectional class.\n'

        try:
            combining_class = unicodedata2.combining(character)
            combining_name = combining_classes.get(combining_class, '[Unknown combining class name]')
            description += f'Combining class: {combining_name} ({combining_class})\n'
        except:
            description += 'Unexpected error while getting combining class.\n'

        try:
            east_asian_width = unicodedata2.east_asian_width(character)
            east_asian_name = east_asian_width_classes.get(east_asian_width, '[Unknown east asian width name]')
            description += f'East asian width: {east_asian_name} ({east_asian_width})\n'
        except:
            description += 'Unexpected error while getting east asian width.\n'
        
        try:
            mirrorred = unicodedata2.mirrored(character)
            description += f"Is bidirectionally mirrored: {'yes' if mirrorred else 'no'}\n"
        except:
            description += 'Unexpected error while getting bidirectional mirroring.\n'
        
        try:
            decomposition = unicodedata2.decomposition(character)
            if decomposition:
                description += f'Decomposition mapping: `{decomposition}`\n'
            else:
                description += 'Has no decomposition mapping.\n'
        except:
            description += 'Unexpected error while getting decomposition mapping.\n'

        await ctx.reply(description, mention_author=False)