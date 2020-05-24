import re


def is_url(line: str) -> bool:
    '''
    Returns True if line starts with <protocol>://
    '''
    url_regexp = re.compile(r'^\w+://')
    return url_regexp.match(line) is not None
