import re
from typing import List

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage


def createPage(factory: PageFactory,
               alias: str,
               parent_page: WikiPage,
               tags: List[str]) -> WikiPage:
    '''
    Create page with alisas and order correction
    '''
    siblings = [child_page.title for child_page in parent_page.children]
    title = getAlternativeTitle(alias, siblings)
    page = factory.create(parent_page, title, tags)
    if title != alias:
        page.alias = alias

    return page


def getAlternativeTitle(title: str,
                        siblings: List[str],
                        substitution: str = '_',
                        template: str = '{title} ({number})') -> str:
    '''
    The function proposes the page title based on the user title.
    The function replace forbidden characters on the substitution symbol.

    title - original title for the page (with forbidden characters).
    siblings - list of the page titles on the same level.
    substitution - forbidden characters will be replaced to this string.
    template - format string for unique title.

    Return title for the new page.
    '''
    newtitle = title.strip()
    siblings_lower = [sibling.lower().strip() for sibling in siblings]

    # 1. Replace forbidden characters
    regexp = re.compile(r'[><|?*:"\\/#%]')
    newtitle = regexp.sub(substitution, newtitle)

    # 2. Replace double underline in the begin title
    if newtitle.startswith('__'):
        newtitle = '--' + newtitle[2:]

    # 3. Check for special names
    if re.match(r'^\.+$', newtitle):
        newtitle = ''

    # 4. Make unique title
    result = newtitle
    n = 1
    while (len(result.strip()) == 0 or
           result.lower() in siblings_lower):
        result = template.format(title=newtitle, number=n).strip()
        n += 1

    result = result.strip()
    return result
