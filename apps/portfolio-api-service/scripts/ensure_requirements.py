from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

REQUIRED_MODULES = [
    'fastapi',
    'sqlalchemy',
    'pyotp',
    'qrcode',
]


def main() -> int:
    missing = []
    for module_name in REQUIRED_MODULES:
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            missing.append(module_name)

    if not missing:
        return 0

    requirements_path = Path(__file__).resolve().parents[1] / 'requirements.txt'
    print(
        'Missing Python dependencies for portfolio-api-service '
        f'({", ".join(missing)}). Installing from {requirements_path}...',
        file=sys.stderr,
    )
    completed = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_path)],
        check=False,
    )
    return completed.returncode


if __name__ == '__main__':
    raise SystemExit(main())
