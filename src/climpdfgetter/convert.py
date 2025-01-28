# import json
from pathlib import Path

import click

# from .utils import _find_project_root


def _prep_path(item: Path):
    if item.is_file() and not item.name.startswith("."):  # avoid .DS_store and other files
        return Path(item)


@click.command()
@click.argument("source", nargs=1)
def convert(source: Path):
    """
    Convert PDFs in a given directory ``source`` to json. If the input files are of a different format,
    they'll first be converted to PDF.
    """

    from PIL import Image

    # from text_processing.pdf_to_text import pdf2text, text2json
    from tqdm import tqdm

    data_root = Path(source)

    collected_input_files = []

    for directory in data_root.iterdir():
        if directory.is_dir():
            for item in directory.iterdir():
                collected_input_files.append(_prep_path(item))
        else:
            collected_input_files.append(_prep_path(directory))

    click.echo("* Found " + str(len(collected_input_files)) + " input files")

    files_to_convert_to_pdf = [i for i in collected_input_files if i is not None and i.suffix.lower() != ".pdf"]

    if len(files_to_convert_to_pdf):

        click.echo("* Found " + str(len(files_to_convert_to_pdf)) + " files that must first be converted to PDF.")

        success_count = 0
        fail_count = 0

        for i in tqdm(files_to_convert_to_pdf):
            try:
                Image.open(i).save(i.with_suffix(".pdf"), "PDF", save_all=True, resolution=100)
                collected_input_files.append(i.with_suffix(".pdf"))
                success_count += 1
            except ValueError:
                fail_count += 1

        click.echo("* Successfully converted " + str(success_count) + " files to PDF.")
        click.echo("* Failed to convert " + str(fail_count) + " files to PDF.")

    success_count = 0
    fail_count = 0

    # document_converter = DocumentConverter()
    # conversion_results = document_converter.convert_all(collected_input_files, raises_on_error=False)
    # success_count = 0
    # fail_count = 0
    # output_files[0].parent.mkdir(parents=True, exist_ok=True)  # make output data directory
    # for i, result in enumerate(conversion_results):
    #     out_path = output_files[i]
    #     if result.status == ConversionStatus.SUCCESS:
    #         success_count += 1
    #         with open(out_path, "w") as f:
    #             f.write(json.dumps(result.document.export_to_dict()))
    #     else:
    #         fail_count += 1

    click.echo(f"Success count: {success_count}")
    click.echo(f"Fail count: {fail_count}")
