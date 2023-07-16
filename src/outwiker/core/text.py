# -*- coding: utf-8 -*-

from typing import Any, Dict


def dictToStr(paramsDict: Dict[str, Any]) -> str:
    """
    Return string like param_1="value1" param_2='value "" with double quotes'...
    """
    items = []
    for name, value in paramsDict.items():
        valueStr = str(value)

        hasSingleQuote = "'" in valueStr
        hasDoubleQuote = '"' in valueStr

        if hasSingleQuote and hasDoubleQuote:
            valueStr = valueStr.replace('"', '\\"')
            quote = '"'
        elif hasDoubleQuote:
            quote = "'"
        else:
            quote = '"'

        paramStr = '{name}={quote}{value}{quote}'.format(
            name=name,
            quote=quote,
            value=valueStr
        )

        items.append(paramStr)

    items.sort()
    return ', '.join(items)

