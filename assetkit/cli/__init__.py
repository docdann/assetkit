import argparse

try:  # optional shell completion via argcomplete
    import argcomplete  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    argcomplete = None


def main():
    from . import new
    from . import scaffold
    from assetkit.internal.cli.bundle_docker_image import register_bundle_docker_image_command
    from assetkit.internal.cli.load_docker_image import register_load_docker_image_command
    from assetkit.internal.cli.export_package import register_export_package_command
    from assetkit.internal.cli.combine_packages import register_combine_command
    from .registry import register_registry_command

    parser = argparse.ArgumentParser(prog="assetkit", description="AssetKit CLI")
    subparsers = parser.add_subparsers(dest="command")

    new.register_new_command(subparsers)
    scaffold.register_scaffold_command(subparsers)
    register_bundle_docker_image_command(subparsers)
    register_load_docker_image_command(subparsers)
    register_export_package_command(subparsers)
    register_combine_command(subparsers)
    register_registry_command(subparsers)

    if argcomplete:
        argcomplete.autocomplete(parser)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
