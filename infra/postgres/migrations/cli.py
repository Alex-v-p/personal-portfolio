from __future__ import annotations

import argparse
import logging

from infra.postgres.migrations.manager import create_revision, migration_smoke_check, stamp_database, upgrade_database

logging.basicConfig(level=logging.INFO)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Portfolio database migration helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upgrade = subparsers.add_parser("upgrade", help="Apply migrations up to a revision.")
    upgrade.add_argument("revision", nargs="?", default="head")

    stamp = subparsers.add_parser("stamp", help="Mark the database at a revision without running migration SQL.")
    stamp.add_argument("revision", nargs="?", default="head")

    revision = subparsers.add_parser("revision", help="Create a migration revision file.")
    revision.add_argument("-m", "--message", required=True)
    revision.add_argument("--autogenerate", action="store_true")

    subparsers.add_parser("check", help="Run a migration smoke check against a temp SQLite database.")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "upgrade":
        upgrade_database(revision=args.revision)
        return 0

    if args.command == "stamp":
        stamp_database(revision=args.revision)
        return 0

    if args.command == "revision":
        create_revision(message=args.message, autogenerate=args.autogenerate)
        return 0

    if args.command == "check":
        migration_smoke_check()
        return 0

    raise RuntimeError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
