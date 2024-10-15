import os
from process import process_images
from model import images_to_vox


def main():
    directory_path = '/home/kowkodivka/Документы/hist_image_analyzer/photo/raw/'
    output_directory = '/home/kowkodivka/Документы/hist_image_analyzer/photo/processed/'
    raw_regex_pattern = r'photo_\d+_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.jpg'
    proc_regex_pattern = r'processed_photo_\d+_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.png'

    if os.listdir(directory_path) == 0:
        process_images(directory_path, output_directory, raw_regex_pattern)
    images_to_vox(output_directory, './output.vox', proc_regex_pattern)


if __name__ == '__main__':
    main()