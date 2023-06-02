from enum import Enum
from typing import Iterable


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


def remap(pairs: Iterable[str], delimiter: str = ':') -> dict[str, str]:
    values: Iterable[tuple] = (
        tuple(map(str.strip, pair.split(delimiter))) for pair in (pairs or ()) if pair
    )
    return dict(values)
