from os import sep


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