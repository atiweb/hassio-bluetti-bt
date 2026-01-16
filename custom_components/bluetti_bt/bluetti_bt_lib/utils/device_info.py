"""Device info helper."""

from ..devices import DEVICE_NAME_RE


def get_type_by_bt_name(bt_name: str) -> str | None:
    """Check bluetooth name and return type if supported."""

    # Some devices don't show up with a name.  re.match() will fail on None type
    if bt_name is None:
        return None

    match = DEVICE_NAME_RE.match(bt_name)

    if match is None:
        return None

    return match[1]
