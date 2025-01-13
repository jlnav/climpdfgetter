import json
from pathlib import Path

import click
from docling.document_converter import DocumentConverter

from .utils import _find_project_root


def _prep_path(item: Path):
    if item.is_file() and not item.name.startswith("."):  # avoid .DS_store and other files
        if not item.suffix == ".txt":
            return Path(item)
        else:
            return Path(item).rename(item.with_suffix(".html"))


@click.command()
@click.argument("source", nargs=1)
def convert(source: Path):
    """Convert eligible files in a given directory ``source`` to json."""

    # either take a directory, or list of directories each containing files to convert
    data_root = Path(source)

    collected_input_files = []

    for directory in data_root.iterdir():
        if directory.is_dir():
            for item in directory.iterdir():
                collected_input_files.append(_prep_path(item))
        else:
            collected_input_files.append(_prep_path(directory))

    output_files = [
        Path(_find_project_root()) / Path("json") / Path(Path(i).stem + ".json") for i in collected_input_files
    ]

    document_converter = DocumentConverter()
    conversion_results = document_converter.convert_all(collected_input_files)

    for i, result in enumerate(conversion_results):
        out_path = output_files[i]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            f.write(json.dumps(result.document.export_to_dict()))
