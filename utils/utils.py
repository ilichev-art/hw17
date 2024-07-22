from pathlib import Path


def schema_path(name):
    return str(Path(__file__).parent.parent.joinpath(f'schemas/{name}'))