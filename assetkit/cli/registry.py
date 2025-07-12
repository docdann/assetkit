import argparse
from pathlib import Path

from assetkit.registry import push_package, pull_package, list_packages

try:  # optional bash completion via argcomplete
    import argcomplete
except ImportError:  # pragma: no cover - argcomplete optional
    argcomplete = None


def register_registry_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("registry", help="Interact with AssetKit registry")
    reg_sub = parser.add_subparsers(dest="subcommand")

    push_p = reg_sub.add_parser("push", help="Push a package directory or archive")
    push_p.add_argument("path", help="Path to package directory or tar.gz archive")
    push_p.set_defaults(func=registry_push)

    pull_p = reg_sub.add_parser("pull", help="Pull a package from the registry")
    name_arg = pull_p.add_argument("name", help="Package name (with or without .tar.gz)")
    if argcomplete:
        def completer(prefix, parsed_args, **_):
            return [p for p in list_packages() if p.startswith(prefix)]
        name_arg.completer = completer
    pull_p.add_argument("--output", default=".", help="Directory to extract to")
    pull_p.set_defaults(func=registry_pull)

    list_p = reg_sub.add_parser("list", help="List packages in the registry")
    list_p.set_defaults(func=registry_list)


def registry_push(args):
    path = Path(args.path).resolve()
    push_package(path)


def registry_pull(args):
    output = Path(args.output).resolve()
    pull_package(args.name, output)


def registry_list(args):
    for name in list_packages():
        print(name)
