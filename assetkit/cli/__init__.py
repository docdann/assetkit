import argparse

def main():
    from . import new
    from . import scaffold
    from assetkit.internal.cli.bundle_docker_image import register_bundle_docker_image_command
    from assetkit.internal.cli.load_docker_image import register_load_docker_image_command

    parser = argparse.ArgumentParser(prog="assetkit", description="AssetKit CLI")
    subparsers = parser.add_subparsers(dest="command")

    new.register_new_command(subparsers)
    scaffold.register_scaffold_command(subparsers)
    register_bundle_docker_image_command(subparsers)
    register_load_docker_image_command(subparsers)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
