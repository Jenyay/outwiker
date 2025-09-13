from outwiker.pages.wiki.parser.wikiparser import Parser


def get_styles_count(parser: Parser, css_class: str) -> int:
    find_style_count = 0
    for style in parser.styleItems:
        if css_class in style:
            find_style_count += 1

    return find_style_count

