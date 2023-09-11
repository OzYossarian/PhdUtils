from pathlib import Path

from main import combine_pdfs, convert_pdf_to_images_and_back

dpi = 200
jpg_quality = 95

pdf_stems = [
    'QPL 2023 Talk - Intro.pdf',
    'QPL 2023 Talk - Pauli Webs.pdf',
    'QPL 2023 Talk - Measurement.pdf',
    'QPL 2023 Talk - Detectors, Logicals.pdf',
    'QPL 2023 Talk - More Detectors and Logicals.pdf',
    'QPL 2023 Talk - Floquetifying 4,2,2.pdf',
    # 'QPL 2023 Talk - Floquetifying Colour Code.pdf',
    'QPL 2023 Talk - Outro.pdf']
base_path = Path('/Users/teague/Documents/PhD/Talks/QPL_2023_Talk/')
pdf_paths = [base_path / Path(stem) for stem in pdf_stems]
combined_name = base_path / Path('QPL_2023_Talk.pdf')
combine_pdfs(pdf_paths, combined_name)
#
pdf_path = Path('/Users/teague/Documents/PhD/Talks/QPL_2023_Talk/QPL_2023_Talk.pdf')
convert_pdf_to_images_and_back(pdf_path, 'png', 200)
