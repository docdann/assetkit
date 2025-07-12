# AssetKit Documentation

AssetKit is a toolkit for structured runtime asset packaging and discovery.

## Getting Started
Install AssetKit via pip:
```
pip install assetkit
```

Create new asset packages using the CLI:
```
assetkit new myplugin        # or `python -m assetkit new myplugin`
```

Manage packages in the local registry:
```
assetkit registry push myplugin
assetkit registry list
assetkit registry pull myplugin --output ./fetched
```

To enable tab-completion of registry package names, install `argcomplete` and run `activate-global-python-argcomplete --user`.


See `USAGE.md` for a full guide.
