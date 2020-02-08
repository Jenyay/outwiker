"""
Utility functions for working with the color names and color value
formats defined by the HTML and CSS specifications for use in
documents on the Web.

See documentation (in docs/ directory of source distribution) for
details of the supported formats, conventions and conversions.

"""

import collections
import re
import string
import struct

import six


__version__ = '1.10'


def _reversedict(d):
    """
    Internal helper for generating reverse mappings; given a
    dictionary, returns a new dictionary with keys and values swapped.

    """
    return {value: key for key, value in d.items()}


HEX_COLOR_RE = re.compile(r'^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$')

HTML4 = u'html4'
CSS2 = u'css2'
CSS21 = u'css21'
CSS3 = u'css3'

SUPPORTED_SPECIFICATIONS = (HTML4, CSS2, CSS21, CSS3)

SPECIFICATION_ERROR_TEMPLATE = u'{{spec}} is not a supported specification for color name lookups; \
supported specifications are: {supported}.'.format(
    supported=','.join(SUPPORTED_SPECIFICATIONS)
)


IntegerRGB = collections.namedtuple('IntegerRGB', ['red', 'green', 'blue'])

PercentRGB = collections.namedtuple('PercentRGB', ['red', 'green', 'blue'])

HTML5SimpleColor = collections.namedtuple(
    'HTML5SimpleColor', ['red', 'green', 'blue']
)


# Mappings of color names to normalized hexadecimal color values.
#################################################################

# The HTML 4 named colors.
#
# The canonical source for these color definitions is the HTML 4
# specification:
#
# http://www.w3.org/TR/html401/types.html#h-6.5
#
# The file tests/definitions.py in the source distribution of this
# module downloads a copy of the HTML 4 standard and parses out the
# color names to ensure the values below are correct.
HTML4_NAMES_TO_HEX = {
    u'aqua': u'#00ffff',
    u'black': u'#000000',
    u'blue': u'#0000ff',
    u'fuchsia': u'#ff00ff',
    u'green': u'#008000',
    u'gray': u'#808080',
    u'lime': u'#00ff00',
    u'maroon': u'#800000',
    u'navy': u'#000080',
    u'olive': u'#808000',
    u'purple': u'#800080',
    u'red': u'#ff0000',
    u'silver': u'#c0c0c0',
    u'teal': u'#008080',
    u'white': u'#ffffff',
    u'yellow': u'#ffff00',
}

# CSS 2 used the same list as HTML 4.
CSS2_NAMES_TO_HEX = HTML4_NAMES_TO_HEX

# CSS 2.1 added orange.
CSS21_NAMES_TO_HEX = dict(HTML4_NAMES_TO_HEX, orange=u'#ffa500')

# The CSS 3/SVG named colors.
#
# The canonical source for these color definitions is the SVG
# specification's color list (which was adopted as CSS 3's color
# definition):
#
# http://www.w3.org/TR/SVG11/types.html#ColorKeywords
#
# CSS 3 also provides definitions of these colors:
#
# http://www.w3.org/TR/css3-color/#svg-color
#
# SVG provides the definitions as RGB triplets. CSS 3 provides them
# both as RGB triplets and as hexadecimal. Since hex values are more
# common in real-world HTML and CSS, the mapping below is to hex
# values instead. The file tests/definitions.py in the source
# distribution of this module downloads a copy of the CSS 3 color
# module and parses out the color names to ensure the values below are
# correct.
CSS3_NAMES_TO_HEX = {
    u'aliceblue': u'#f0f8ff',
    u'antiquewhite': u'#faebd7',
    u'aqua': u'#00ffff',
    u'aquamarine': u'#7fffd4',
    u'azure': u'#f0ffff',
    u'beige': u'#f5f5dc',
    u'bisque': u'#ffe4c4',
    u'black': u'#000000',
    u'blanchedalmond': u'#ffebcd',
    u'blue': u'#0000ff',
    u'blueviolet': u'#8a2be2',
    u'brown': u'#a52a2a',
    u'burlywood': u'#deb887',
    u'cadetblue': u'#5f9ea0',
    u'chartreuse': u'#7fff00',
    u'chocolate': u'#d2691e',
    u'coral': u'#ff7f50',
    u'cornflowerblue': u'#6495ed',
    u'cornsilk': u'#fff8dc',
    u'crimson': u'#dc143c',
    u'cyan': u'#00ffff',
    u'darkblue': u'#00008b',
    u'darkcyan': u'#008b8b',
    u'darkgoldenrod': u'#b8860b',
    u'darkgray': u'#a9a9a9',
    u'darkgrey': u'#a9a9a9',
    u'darkgreen': u'#006400',
    u'darkkhaki': u'#bdb76b',
    u'darkmagenta': u'#8b008b',
    u'darkolivegreen': u'#556b2f',
    u'darkorange': u'#ff8c00',
    u'darkorchid': u'#9932cc',
    u'darkred': u'#8b0000',
    u'darksalmon': u'#e9967a',
    u'darkseagreen': u'#8fbc8f',
    u'darkslateblue': u'#483d8b',
    u'darkslategray': u'#2f4f4f',
    u'darkslategrey': u'#2f4f4f',
    u'darkturquoise': u'#00ced1',
    u'darkviolet': u'#9400d3',
    u'deeppink': u'#ff1493',
    u'deepskyblue': u'#00bfff',
    u'dimgray': u'#696969',
    u'dimgrey': u'#696969',
    u'dodgerblue': u'#1e90ff',
    u'firebrick': u'#b22222',
    u'floralwhite': u'#fffaf0',
    u'forestgreen': u'#228b22',
    u'fuchsia': u'#ff00ff',
    u'gainsboro': u'#dcdcdc',
    u'ghostwhite': u'#f8f8ff',
    u'gold': u'#ffd700',
    u'goldenrod': u'#daa520',
    u'gray': u'#808080',
    u'grey': u'#808080',
    u'green': u'#008000',
    u'greenyellow': u'#adff2f',
    u'honeydew': u'#f0fff0',
    u'hotpink': u'#ff69b4',
    u'indianred': u'#cd5c5c',
    u'indigo': u'#4b0082',
    u'ivory': u'#fffff0',
    u'khaki': u'#f0e68c',
    u'lavender': u'#e6e6fa',
    u'lavenderblush': u'#fff0f5',
    u'lawngreen': u'#7cfc00',
    u'lemonchiffon': u'#fffacd',
    u'lightblue': u'#add8e6',
    u'lightcoral': u'#f08080',
    u'lightcyan': u'#e0ffff',
    u'lightgoldenrodyellow': u'#fafad2',
    u'lightgray': u'#d3d3d3',
    u'lightgrey': u'#d3d3d3',
    u'lightgreen': u'#90ee90',
    u'lightpink': u'#ffb6c1',
    u'lightsalmon': u'#ffa07a',
    u'lightseagreen': u'#20b2aa',
    u'lightskyblue': u'#87cefa',
    u'lightslategray': u'#778899',
    u'lightslategrey': u'#778899',
    u'lightsteelblue': u'#b0c4de',
    u'lightyellow': u'#ffffe0',
    u'lime': u'#00ff00',
    u'limegreen': u'#32cd32',
    u'linen': u'#faf0e6',
    u'magenta': u'#ff00ff',
    u'maroon': u'#800000',
    u'mediumaquamarine': u'#66cdaa',
    u'mediumblue': u'#0000cd',
    u'mediumorchid': u'#ba55d3',
    u'mediumpurple': u'#9370db',
    u'mediumseagreen': u'#3cb371',
    u'mediumslateblue': u'#7b68ee',
    u'mediumspringgreen': u'#00fa9a',
    u'mediumturquoise': u'#48d1cc',
    u'mediumvioletred': u'#c71585',
    u'midnightblue': u'#191970',
    u'mintcream': u'#f5fffa',
    u'mistyrose': u'#ffe4e1',
    u'moccasin': u'#ffe4b5',
    u'navajowhite': u'#ffdead',
    u'navy': u'#000080',
    u'oldlace': u'#fdf5e6',
    u'olive': u'#808000',
    u'olivedrab': u'#6b8e23',
    u'orange': u'#ffa500',
    u'orangered': u'#ff4500',
    u'orchid': u'#da70d6',
    u'palegoldenrod': u'#eee8aa',
    u'palegreen': u'#98fb98',
    u'paleturquoise': u'#afeeee',
    u'palevioletred': u'#db7093',
    u'papayawhip': u'#ffefd5',
    u'peachpuff': u'#ffdab9',
    u'peru': u'#cd853f',
    u'pink': u'#ffc0cb',
    u'plum': u'#dda0dd',
    u'powderblue': u'#b0e0e6',
    u'purple': u'#800080',
    u'red': u'#ff0000',
    u'rosybrown': u'#bc8f8f',
    u'royalblue': u'#4169e1',
    u'saddlebrown': u'#8b4513',
    u'salmon': u'#fa8072',
    u'sandybrown': u'#f4a460',
    u'seagreen': u'#2e8b57',
    u'seashell': u'#fff5ee',
    u'sienna': u'#a0522d',
    u'silver': u'#c0c0c0',
    u'skyblue': u'#87ceeb',
    u'slateblue': u'#6a5acd',
    u'slategray': u'#708090',
    u'slategrey': u'#708090',
    u'snow': u'#fffafa',
    u'springgreen': u'#00ff7f',
    u'steelblue': u'#4682b4',
    u'tan': u'#d2b48c',
    u'teal': u'#008080',
    u'thistle': u'#d8bfd8',
    u'tomato': u'#ff6347',
    u'turquoise': u'#40e0d0',
    u'violet': u'#ee82ee',
    u'wheat': u'#f5deb3',
    u'white': u'#ffffff',
    u'whitesmoke': u'#f5f5f5',
    u'yellow': u'#ffff00',
    u'yellowgreen': u'#9acd32',
}


# Mappings of normalized hexadecimal color values to color names.
#################################################################

HTML4_HEX_TO_NAMES = _reversedict(HTML4_NAMES_TO_HEX)

CSS2_HEX_TO_NAMES = HTML4_HEX_TO_NAMES

CSS21_HEX_TO_NAMES = _reversedict(CSS21_NAMES_TO_HEX)

CSS3_HEX_TO_NAMES = _reversedict(CSS3_NAMES_TO_HEX)

# CSS3 defines both 'gray' and 'grey', as well as defining either
# variant for other related colors like 'darkgray'/'darkgrey'. For a
# 'forward' lookup from name to hex, this is straightforward, but a
# 'reverse' lookup from hex to name requires picking one spelling.
#
# The way in which _reversedict() generates the reverse mappings will
# pick a spelling based on the ordering of dictionary keys, which
# varies according to the version and implementation of Python in use,
# and in some Python versions is explicitly not to be relied on for
# consistency. So here we manually pick a single spelling that will
# consistently be returned. Since 'gray' was the only spelling
# supported in HTML 4, CSS1, and CSS2, 'gray' and its varients are
# chosen.
CSS3_HEX_TO_NAMES[u'#a9a9a9'] = u'darkgray'
CSS3_HEX_TO_NAMES[u'#2f4f4f'] = u'darkslategray'
CSS3_HEX_TO_NAMES[u'#696969'] = u'dimgray'
CSS3_HEX_TO_NAMES[u'#808080'] = u'gray'
CSS3_HEX_TO_NAMES[u'#d3d3d3'] = u'lightgray'
CSS3_HEX_TO_NAMES[u'#778899'] = u'lightslategray'
CSS3_HEX_TO_NAMES[u'#708090'] = u'slategray'


# Aliases of the above mappings, for backwards compatibility.
#################################################################
(html4_names_to_hex,
 css2_names_to_hex,
 css21_names_to_hex,
 css3_names_to_hex) = (HTML4_NAMES_TO_HEX,
                       CSS2_NAMES_TO_HEX,
                       CSS21_NAMES_TO_HEX,
                       CSS3_NAMES_TO_HEX)

(html4_hex_to_names,
 css2_hex_to_names,
 css21_hex_to_names,
 css3_hex_to_names) = (HTML4_HEX_TO_NAMES,
                       CSS2_HEX_TO_NAMES,
                       CSS21_HEX_TO_NAMES,
                       CSS3_HEX_TO_NAMES)


# Normalization functions.
#################################################################

def normalize_hex(hex_value):
    """
    Normalize a hexadecimal color value to 6 digits, lowercase.

    """
    match = HEX_COLOR_RE.match(hex_value)
    if match is None:
        raise ValueError(
            u"'{}' is not a valid hexadecimal color value.".format(hex_value)
        )
    hex_digits = match.group(1)
    if len(hex_digits) == 3:
        hex_digits = u''.join(2 * s for s in hex_digits)
    return u'#{}'.format(hex_digits.lower())


def _normalize_integer_rgb(value):
    """
    Internal normalization function for clipping integer values into
    the permitted range (0-255, inclusive).

    """
    return 0 if value < 0 \
        else 255 if value > 255 \
        else value


def normalize_integer_triplet(rgb_triplet):
    """
    Normalize an integer ``rgb()`` triplet so that all values are
    within the range 0-255 inclusive.

    """
    return IntegerRGB._make(
        _normalize_integer_rgb(value) for value in rgb_triplet
    )


def _normalize_percent_rgb(value):
    """
    Internal normalization function for clipping percent values into
    the permitted range (0%-100%, inclusive).

    """
    percent = value.split(u'%')[0]
    percent = float(percent) if u'.' in percent else int(percent)

    return u'0%' if percent < 0 \
        else u'100%' if percent > 100 \
        else u'{}%'.format(percent)


def normalize_percent_triplet(rgb_triplet):
    """
    Normalize a percentage ``rgb()`` triplet so that all values are
    within the range 0%-100% inclusive.

    """
    return PercentRGB._make(
        _normalize_percent_rgb(value) for value in rgb_triplet
    )


# Conversions from color names to various formats.
#################################################################

def name_to_hex(name, spec=CSS3):
    """
    Convert a color name to a normalized hexadecimal color value.

    The optional keyword argument ``spec`` determines which
    specification's list of color names will be used. The default is
    CSS3.

    When no color of that name exists in the given specification,
    ``ValueError`` is raised.

    """
    if spec not in SUPPORTED_SPECIFICATIONS:
        raise ValueError(SPECIFICATION_ERROR_TEMPLATE.format(spec=spec))
    normalized = name.lower()
    hex_value = {
        CSS2: CSS2_NAMES_TO_HEX,
        CSS21: CSS21_NAMES_TO_HEX,
        CSS3: CSS3_NAMES_TO_HEX,
        HTML4: HTML4_NAMES_TO_HEX
    }[spec].get(normalized)
    if hex_value is None:
        raise ValueError(
            u"'{name}' is not defined as a named color in {spec}".format(
                name=name, spec=spec
            )
        )
    return hex_value


def name_to_rgb(name, spec=CSS3):
    """
    Convert a color name to a 3-tuple of integers suitable for use in
    an ``rgb()`` triplet specifying that color.

    """
    return hex_to_rgb(name_to_hex(name, spec=spec))


def name_to_rgb_percent(name, spec=CSS3):
    """
    Convert a color name to a 3-tuple of percentages suitable for use
    in an ``rgb()`` triplet specifying that color.

    """
    return rgb_to_rgb_percent(name_to_rgb(name, spec=spec))


# Conversions from hexadecimal color values to various formats.
#################################################################

def hex_to_name(hex_value, spec=CSS3):
    """
    Convert a hexadecimal color value to its corresponding normalized
    color name, if any such name exists.

    The optional keyword argument ``spec`` determines which
    specification's list of color names will be used. The default is
    CSS3.

    When no color name for the value is found in the given
    specification, ``ValueError`` is raised.

    """
    if spec not in SUPPORTED_SPECIFICATIONS:
        raise ValueError(SPECIFICATION_ERROR_TEMPLATE.format(spec=spec))
    normalized = normalize_hex(hex_value)
    name = {
        CSS2: CSS2_HEX_TO_NAMES,
        CSS21: CSS21_HEX_TO_NAMES,
        CSS3: CSS3_HEX_TO_NAMES,
        HTML4: HTML4_HEX_TO_NAMES
    }[spec].get(normalized)
    if name is None:
        raise ValueError(
            u"'{}' has no defined color name in {}".format(hex_value, spec)
        )
    return name


def hex_to_rgb(hex_value):
    """
    Convert a hexadecimal color value to a 3-tuple of integers
    suitable for use in an ``rgb()`` triplet specifying that color.

    """
    hex_value = normalize_hex(hex_value)
    hex_value = int(hex_value[1:], 16)
    return IntegerRGB(
        hex_value >> 16,
        hex_value >> 8 & 0xff,
        hex_value & 0xff
    )


def hex_to_rgb_percent(hex_value):
    """
    Convert a hexadecimal color value to a 3-tuple of percentages
    suitable for use in an ``rgb()`` triplet representing that color.

    """
    return rgb_to_rgb_percent(hex_to_rgb(hex_value))


# Conversions from  integer rgb() triplets to various formats.
#################################################################

def rgb_to_name(rgb_triplet, spec=CSS3):
    """
    Convert a 3-tuple of integers, suitable for use in an ``rgb()``
    color triplet, to its corresponding normalized color name, if any
    such name exists.

    The optional keyword argument ``spec`` determines which
    specification's list of color names will be used. The default is
    CSS3.

    If there is no matching name, ``ValueError`` is raised.

    """
    return hex_to_name(
        rgb_to_hex(
            normalize_integer_triplet(
                rgb_triplet
            )
        ),
        spec=spec
    )


def rgb_to_hex(rgb_triplet):
    """
    Convert a 3-tuple of integers, suitable for use in an ``rgb()``
    color triplet, to a normalized hexadecimal value for that color.

    """
    return u'#{:02x}{:02x}{:02x}'.format(
        *normalize_integer_triplet(
            rgb_triplet
        )
    )


def rgb_to_rgb_percent(rgb_triplet):
    """
    Convert a 3-tuple of integers, suitable for use in an ``rgb()``
    color triplet, to a 3-tuple of percentages suitable for use in
    representing that color.

    This function makes some trade-offs in terms of the accuracy of
    the final representation; for some common integer values,
    special-case logic is used to ensure a precise result (e.g.,
    integer 128 will always convert to '50%', integer 32 will always
    convert to '12.5%'), but for all other values a standard Python
    ``float`` is used and rounded to two decimal places, which may
    result in a loss of precision for some values.

    """
    # In order to maintain precision for common values,
    # special-case them.
    specials = {255: u'100%', 128: u'50%', 64: u'25%',
                32: u'12.5%', 16: u'6.25%', 0: u'0%'}
    return PercentRGB._make(
        specials.get(d, u'{:.02f}%'.format(d / 255.0 * 100))
        for d in normalize_integer_triplet(rgb_triplet)
    )


# Conversions from percentage rgb() triplets to various formats.
#################################################################

def rgb_percent_to_name(rgb_percent_triplet, spec=CSS3):
    """
    Convert a 3-tuple of percentages, suitable for use in an ``rgb()``
    color triplet, to its corresponding normalized color name, if any
    such name exists.

    The optional keyword argument ``spec`` determines which
    specification's list of color names will be used. The default is
    CSS3.

    If there is no matching name, ``ValueError`` is raised.

    """
    return rgb_to_name(
        rgb_percent_to_rgb(
            normalize_percent_triplet(
                rgb_percent_triplet
            )
        ),
        spec=spec
    )


def rgb_percent_to_hex(rgb_percent_triplet):
    """
    Convert a 3-tuple of percentages, suitable for use in an ``rgb()``
    color triplet, to a normalized hexadecimal color value for that
    color.

    """
    return rgb_to_hex(
        rgb_percent_to_rgb(
            normalize_percent_triplet(
                rgb_percent_triplet
            )
        )
    )


def _percent_to_integer(percent):
    """
    Internal helper for converting a percentage value to an integer
    between 0 and 255 inclusive.

    """
    return int(
        round(
            float(percent.split(u'%')[0]) / 100 * 255
        )
    )


def rgb_percent_to_rgb(rgb_percent_triplet):
    """
    Convert a 3-tuple of percentages, suitable for use in an ``rgb()``
    color triplet, to a 3-tuple of integers suitable for use in
    representing that color.

    Some precision may be lost in this conversion. See the note
    regarding precision for ``rgb_to_rgb_percent()`` for details.

    """
    return IntegerRGB._make(
        map(
            _percent_to_integer,
            normalize_percent_triplet(
                rgb_percent_triplet
            )
        )
    )


# HTML5 color algorithms.
#################################################################

# These functions are written in a way that may seem strange to
# developers familiar with Python, because they do not use the most
# efficient or idiomatic way of accomplishing their tasks. This is
# because, for compliance, these functions are written as literal
# translations into Python of the algorithms in HTML5.
#
# For ease of understanding, the relevant steps of the algorithm from
# the standard are included as comments interspersed in the
# implementation.

def html5_parse_simple_color(input):
    """
    Apply the simple color parsing algorithm from section 2.4.6 of
    HTML5.

    """
    # 1. Let input be the string being parsed.
    #
    # 2. If input is not exactly seven characters long, then return an
    #    error.
    if not isinstance(input, six.text_type) or len(input) != 7:
        raise ValueError(
            u"An HTML5 simple color must be a Unicode string "
            u"exactly seven characters long."
        )

    # 3. If the first character in input is not a U+0023 NUMBER SIGN
    #    character (#), then return an error.
    if not input.startswith('#'):
        raise ValueError(
            u"An HTML5 simple color must begin with the "
            u"character '#' (U+0023)."
        )

    # 4. If the last six characters of input are not all ASCII hex
    #    digits, then return an error.
    if not all(c in string.hexdigits for c in input[1:]):
        raise ValueError(
            u"An HTML5 simple color must contain exactly six ASCII hex digits."
        )

    # 5. Let result be a simple color.
    #
    # 6. Interpret the second and third characters as a hexadecimal
    #    number and let the result be the red component of result.
    #
    # 7. Interpret the fourth and fifth characters as a hexadecimal
    #    number and let the result be the green component of result.
    #
    # 8. Interpret the sixth and seventh characters as a hexadecimal
    #    number and let the result be the blue component of result.
    #
    # 9. Return result.
    return HTML5SimpleColor(
        int(input[1:3], 16),
        int(input[3:5], 16),
        int(input[5:7], 16)
    )


def html5_serialize_simple_color(simple_color):
    """
    Apply the serialization algorithm for a simple color from section
    2.4.6 of HTML5.

    """
    red, green, blue = simple_color

    # 1. Let result be a string consisting of a single "#" (U+0023)
    #    character.
    result = u'#'

    # 2. Convert the red, green, and blue components in turn to
    #    two-digit hexadecimal numbers using lowercase ASCII hex
    #    digits, zero-padding if necessary, and append these numbers
    #    to result, in the order red, green, blue.
    format_string = '{:02x}'
    result += format_string.format(red)
    result += format_string.format(green)
    result += format_string.format(blue)

    # 3. Return result, which will be a valid lowercase simple color.
    return result


def html5_parse_legacy_color(input):
    """
    Apply the legacy color parsing algorithm from section 2.4.6 of
    HTML5.

    """
    # 1. Let input be the string being parsed.
    if not isinstance(input, six.text_type):
        raise ValueError(
            u"HTML5 legacy color parsing requires a Unicode string as input."
        )

    # 2. If input is the empty string, then return an error.
    if input == "":
        raise ValueError(
            u"HTML5 legacy color parsing forbids empty string as a value."
        )

    # 3. Strip leading and trailing whitespace from input.
    input = input.strip()

    # 4. If input is an ASCII case-insensitive match for the string
    #    "transparent", then return an error.
    if input.lower() == u"transparent":
        raise ValueError(
            u'HTML5 legacy color parsing forbids "transparent" as a value.'
        )

    # 5. If input is an ASCII case-insensitive match for one of the
    #    keywords listed in the SVG color keywords section of the CSS3
    #    Color specification, then return the simple color
    #    corresponding to that keyword.
    keyword_hex = CSS3_NAMES_TO_HEX.get(input.lower())
    if keyword_hex is not None:
        return html5_parse_simple_color(keyword_hex)

    # 6. If input is four characters long, and the first character in
    #    input is a "#" (U+0023) character, and the last three
    #    characters of input are all ASCII hex digits, then run these
    #    substeps:
    if len(input) == 4 and \
       input.startswith(u'#') and \
       all(c in string.hexdigits for c in input[1:]):
        # 1. Let result be a simple color.
        #
        # 2. Interpret the second character of input as a hexadecimal
        #    digit; let the red component of result be the resulting
        #    number multiplied by 17.
        #
        # 3. Interpret the third character of input as a hexadecimal
        #    digit; let the green component of result be the resulting
        #    number multiplied by 17.
        #
        # 4. Interpret the fourth character of input as a hexadecimal
        #    digit; let the blue component of result be the resulting
        #    number multiplied by 17.
        result = HTML5SimpleColor(
            int(input[1], 16) * 17,
            int(input[2], 16) * 17,
            int(input[3], 16) * 17
        )

        # 5. Return result.
        return result

    # 7. Replace any characters in input that have a Unicode code
    #    point greater than U+FFFF (i.e. any characters that are not
    #    in the basic multilingual plane) with the two-character
    #    string "00".

    # This one's a bit weird due to the existence of multiple internal
    # Unicode string representations in different versions and builds
    # of Python.
    #
    # From Python 2.2 through 3.2, Python could be compiled with
    # "narrow" or "wide" Unicode strings (see PEP 261). Narrow builds
    # handled Unicode strings with two-byte characters and surrogate
    # pairs for non-BMP code points. Wide builds handled Unicode
    # strings with four-byte characters and no surrogates. This means
    # ord() is only sufficient to identify a non-BMP character on a
    # wide build.
    #
    # Starting with Python 3.3, the internal string representation
    # (see PEP 393) is now dynamic, and Python chooses an encoding --
    # either latin-1, UCS-2 or UCS-4 -- wide enough to handle the
    # highest code point in the string.
    #
    # The code below bypasses all of that for a consistently effective
    # method: encode the string to little-endian UTF-32, then perform
    # a binary unpack of it as four-byte integers. Those integers will
    # be the Unicode code points, and from there filtering out non-BMP
    # code points is easy.
    encoded_input = input.encode('utf_32_le')

    # Format string is '<' (for little-endian byte order), then a
    # sequence of 'L' characters (for 4-byte unsigned long integer)
    # equal to the length of the original string, which is also
    # one-fourth the encoded length.  For example, for a six-character
    # input the generated format string will be '<LLLLLL'.
    format_string = '<' + ('L' * (int(len(encoded_input) / 4)))
    codepoints = struct.unpack(format_string, encoded_input)
    input = ''.join(u'00' if c > 0xffff
                    else six.unichr(c)
                    for c in codepoints)

    # 8. If input is longer than 128 characters, truncate input,
    #    leaving only the first 128 characters.
    if len(input) > 128:
        input = input[:128]

    # 9. If the first character in input is a "#" (U+0023) character,
    #    remove it.
    if input.startswith(u'#'):
        input = input[1:]

    # 10. Replace any character in input that is not an ASCII hex
    #     digit with the character "0" (U+0030).
    if any(c for c in input if c not in string.hexdigits):
        input = ''.join(c if c in string.hexdigits else u'0' for c in input)

    # 11. While input's length is zero or not a multiple of three,
    #     append a "0" (U+0030) character to input.
    while (len(input) == 0) or (len(input) % 3 != 0):
        input += u'0'

    # 12. Split input into three strings of equal length, to obtain
    #     three components. Let length be the length of those
    #     components (one third the length of input).
    length = int(len(input) / 3)
    red = input[:length]
    green = input[length:length*2]
    blue = input[length*2:]

    # 13. If length is greater than 8, then remove the leading
    #     length-8 characters in each component, and let length be 8.
    if length > 8:
        red, green, blue = (red[length-8:],
                            green[length-8:],
                            blue[length-8:])
        length = 8

    # 14. While length is greater than two and the first character in
    #     each component is a "0" (U+0030) character, remove that
    #     character and reduce length by one.
    while (length > 2) and (red[0] == u'0' and
                            green[0] == u'0' and
                            blue[0] == u'0'):
        red, green, blue = (red[1:],
                            green[1:],
                            blue[1:])
        length -= 1

    # 15. If length is still greater than two, truncate each
    #     component, leaving only the first two characters in each.
    if length > 2:
        red, green, blue = (red[:2],
                            green[:2],
                            blue[:2])

    # 16. Let result be a simple color.
    #
    # 17. Interpret the first component as a hexadecimal number; let
    #     the red component of result be the resulting number.
    #
    # 18. Interpret the second component as a hexadecimal number; let
    #     the green component of result be the resulting number.
    #
    # 19. Interpret the third component as a hexadecimal number; let
    #     the blue component of result be the resulting number.
    #
    # 20. Return result.
    return HTML5SimpleColor(
        int(red, 16),
        int(green, 16),
        int(blue, 16)
    )
