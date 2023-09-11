from typing import Iterable

import fitz

from datetime import datetime
from pathlib import Path

from alive_progress import alive_bar


def get_all_files_in_directory(directory: Path, extensions: Iterable[str] | None):
    if extensions is None:
        # Get every file
        files = [
            file
            for file in directory.resolve().glob(f'**/*')
            if file.is_file()]
    else:
        # Just get files with specified extensions
        files = [
            file
            for extension in extensions
            for file in directory.resolve().glob(f'**/*.{extension}')]
    return files


def replace_file_with_image(file: Path, output: str, dpi: int, jpg_quality: int = 95):
    # `output` must be listed here:
    # https://pymupdf.readthedocs.io/en/latest/pixmap.html#pixmapoutput
    with fitz.open(file) as doc:
        page = doc[0]
        pix = page.get_pixmap(dpi=dpi)
    file.unlink()
    # `jpg_quality` is ignored if output isn't a JPG.
    pix.save(file.with_suffix(f'.{output}'), jpg_quality=jpg_quality)


def convert_pdf_to_image_folder(file: Path, output: str, dpi: int, jpg_quality: int = 95):
    # Create folder with same name as file
    folder = (file.parent / file.stem)
    folder.mkdir()
    with fitz.open(file) as doc:
        length = len(doc)
        with alive_bar(length, force_tty=True) as bar:
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=dpi)
                # `jpg_quality` is ignored if output isn't a JPG.
                pix.save(folder / f'{i}.{output}', jpg_quality=jpg_quality)
                bar()


def convert_pdf_to_images_and_back(file: Path, output: str, dpi: int, jpg_quality: int = 95):
    # Good for compressing!
    with fitz.open(file) as doc:
        # Create a new blank PDF
        with fitz.open() as new_doc:
            length = len(doc)
            with alive_bar(length, force_tty=True) as bar:
                for i, page in enumerate(doc):
                    # Convert PDF to Pixmap.
                    pix = page.get_pixmap(dpi=dpi)
                    # Convert Pixmap to image.
                    # `jpg_quality` is ignored if output isn't a JPG.
                    pix_bytes = pix.tobytes(output=output, jpg_quality=jpg_quality)
                    # Re-open the image with fitz.
                    with fitz.open(output, pix_bytes) as image:
                        rect = image[0].rect
                        # Convert image back to PDF.
                        image_pdf = image.convert_to_pdf()
                        with fitz.open("pdf", image_pdf) as image_doc:
                            # Paste it into the new PDF.
                            new_page = new_doc.new_page(width=rect.width, height=rect.height)
                            new_page.show_pdf_page(rect, image_doc, 0)
                    bar()
            new_file = file.parent / f'{file.stem}_imaged{file.suffix}'
            new_doc.save(new_file)


def deflate_pdf(file: Path, garbage_level: int = 4):
    # From https://github.com/pymupdf/PyMuPDF/discussions/2107
    new_file = file.parent / f'{file.stem}_deflated{file.suffix}'
    with fitz.open(file) as doc:
        doc.save(new_file, garbage=garbage_level, deflate=True)


def combine_pdfs(files: Iterable[Path], combined_file_name: Path = None):
    empty = True
    with fitz.open() as combined:
        for file in files:
            with fitz.open(file) as doc:
                combined.insert_pdf(doc)
            empty = False
            if combined_file_name is None:
                combined_file_name = file.parent / f'{file.stem}_combined.pdf'
        if not empty:
            combined.save(combined_file_name)
