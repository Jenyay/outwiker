from urllib.parse import unquote_plus
from typing import Optional, Dict


class URLMessage:
    def __init__(self, protocol: str, message_name: str, params: Dict[str, str]):
        self.protocol = protocol
        self.message_name = message_name
        self.params = params

    def __repr__(self) -> str:
        return f"URLMessage(protocol={self.protocol!r}, message_name={self.message_name!r}, params={self.params!r})"


def parse_urlmessage(
    url: str, expected_protocol: Optional[str] = None
) -> Optional[URLMessage]:
    """
    Parses a message string of the format:
        <protocol>://event-name?param1=123&param2=qwerty&...

    If expected_protocol is None, the protocol is extracted from the URL.
    If expected_protocol is provided, the URL must start with that exact protocol,
    otherwise the function returns None.

    Returns a URLMessage instance or None on any parsing error or if the protocol does not match expected_protocol.
    Parameter values are URL-decoded (including '+' as space); keys are left as-is.
    """
    # Extract protocol from URL
    sep = url.find("://")
    if sep == -1:
        return None

    protocol = url[:sep]
    if not protocol:
        return None

    # Check expected protocol if provided
    if expected_protocol is not None and protocol != expected_protocol:
        return None

    rest = url[sep + 3 :]  # skip "://"

    if "?" in rest:
        name_part, params_part = rest.split("?", 1)
    else:
        name_part, params_part = rest, ""

    if not name_part:
        return None

    params = {}
    if params_part:
        for pair in params_part.split("&"):
            if not pair:
                continue
            if "=" in pair:
                key, value = pair.split("=", 1)
            else:
                key, value = pair, ""

            try:
                decoded_value = unquote_plus(value)
            except Exception:
                return None

            params[key] = decoded_value

    return URLMessage(protocol, name_part, params)
