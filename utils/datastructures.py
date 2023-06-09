from enum import Enum
from os.path import splitext
from subprocess import PIPE, Popen
from sys import stdout
from typing import Iterable, Iterator, NamedTuple


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)


class NavItem(NamedTuple):
    href: str
    title: str
    attrs: dict = {}
    file: str = '.'

    def is_current_page(self, output_file: str) -> bool:
        return output_file == self.file


def remap(pairs: Iterable[str] | None, delimiter: str = ':') -> dict[str, str]:
    pairs = (pair for pair in pairs or () if pair)
    split_pairs: Iterator[list[str]] = (pair.split(delimiter)[:2] for pair in pairs)
    values: Iterator[tuple[str, str]] = (  # noqa
        tuple(map(str.strip, pair)) for pair in split_pairs  # type: ignore
    )
    return dict(values)


def dict_to_css_variables(values: dict) -> str:
    variables = '; '.join(f'--{var}: {value}' for var, value in values.items())
    return f'style="{variables}"'


def filepath_to_dotnotation(filepath: str) -> str:
    filename, _ = splitext(filepath)
    return filename.replace('/', '.')


def run_subprocess_and_log_stdout(cmd: str) -> None:
    with Popen(cmd, shell=True, stdout=PIPE) as proc:
        while True:
            proc_stdout = proc.stdout.read().decode('utf-8')  # type: ignore
            stdout.write(proc_stdout)
            if proc.poll() is not None:
                break
        proc.terminate()
