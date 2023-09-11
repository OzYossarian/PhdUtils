from pathlib import Path

from main import get_all_files_in_directory, replace_file_with_image

dpi = 175
jpg_quality = 95

valid_extensions = ['pdf', 'jpg', 'jpeg', 'png']
root_path = Path('/users/teague/Desktop/figures copy')

files = get_all_files_in_directory(root_path, valid_extensions)
for file in files:
    replace_file_with_image(file, 'png', dpi, jpg_quality)