import argparse

try:
    import argcomplete
except ImportError:  # pragma: no cover - optional dependency
    argcomplete = None


def register_completion_command(subparsers: argparse._SubParsersAction) -> None:
    """Register the `completion` subcommand."""
    parser = subparsers.add_parser(
        "completion",
        help="Generate a shell completion script for assetkit",
    )
    parser.add_argument(
        "shell",
        choices=["bash", "zsh"],
        nargs="?",
        default="bash",
        help="Shell type (default: bash)",
    )
    parser.set_defaults(func=_completion_command)


def _completion_command(args: argparse.Namespace) -> None:
    if not argcomplete:
        raise SystemExit("argcomplete is not installed")
    print(argcomplete.shellcode("assetkit", shell=args.shell))
