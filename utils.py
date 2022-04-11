import discord
from more_itertools import split_into
import unicodedata2


def split_into_messages(text, separator='\n'):
    """
    Split the text into pieces, such that every piece fits into a single message.
    """

    current_message = ''
    for part in text.split(separator):
        if len(current_message) + len(part) + len(separator) > 2000:
            yield current_message
            current_message = ''
        current_message += part + separator
    yield current_message

def truncate_to_message(text, separator='\n', notice=lambda x: f"... and {x} more lines."):
    """
    Truncate the text to fit into a single message, adding a notice about how many lines were truncated.
    """
    messages = list(split_into_messages(text, separator))
    if len(messages) == 1: return messages
    msg = messages[0].split(separator)
    lines = 0
    for message in messages[1:]:
        lines += len(message.split(separator))

    while len('\n'.join(msg)) > 2000:
        msg.pop()
        lines -= 1
        msg[-1] = notice(lines)

    return '\n'.join(msg)



SPECIAL_CHARS = {'\n': '`\\n`'}

def char_description(char):
    """
    Convert the character into a Markdown line including the character, its codepoint and its name.
    """
    if char in SPECIAL_CHARS:
        escaped = SPECIAL_CHARS[char]
    else:
        escaped = discord.utils.escape_markdown(char)
    
    # The code point is the hex of the char's unicode value, padded to a minimum of 4 chars.
    codepoint = hex(ord(char))[2:].upper().zfill(4)

    try:
        name = unicodedata2.name(char)
    except ValueError:
        # The character is not in the table.
        name = '<unknown>'

    return f'{escaped} `U+{codepoint} {name}`'
