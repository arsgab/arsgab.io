from enum import Enum
from subprocess import PIPE, Popen
from sys import stdout
from typing import Iterable


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


def remap(pairs: Iterable[str], delimiter: str = ':') -> dict[str, str]:
    values: Iterable[tuple] = (
        tuple(map(str.strip, pair.split(delimiter))) for pair in (pairs or ()) if pair
    )
    return dict(values)


def dict_to_css_variables(values: dict) -> str:
    variables = '; '.join(f'--{var}: {value}' for var, value in values.items())
    return f'style="{variables}"'


def run_subprocess_and_log_stdout(cmd: str) -> None:
    with Popen(cmd, shell=True, stdout=PIPE) as proc:
        while True:
            proc_stdout = proc.stdout.read().decode('utf-8')
            stdout.write(proc_stdout)
            if proc.poll() is not None:
                break
        proc.terminate()
