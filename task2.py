import os

from base_logger import logger


def files_merge(input_folder, output_file, filter_string=None):
    """
    Merges files in input_folder
    """
    if not os.path.exists(input_folder):
        logger.info(f"Folder '{input_folder}' does not exist!")
        return

    files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    total_lines = 0
    total_removed = 0

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for f in files:
            filepath = os.path.join(input_folder, f)
            with open(filepath, 'r', encoding='utf-8') as infile:
                for line in infile:
                    total_lines += 1
                    if filter_string and filter_string in line:
                        total_removed += 1
                        continue
                    outfile.write(line)

    logger.info(f"Files are merged!")
    logger.info(f"Proccessed files: {len(files)}")
    logger.info(f"Total number of lines: {total_lines}")
    logger.info(f"Number of removed lines: {total_removed}")
    logger.info(f"Saved lines: {total_lines - total_removed}")


def main():
    # Пример использования:
    files_merge("generated_files", "result.csv", "abc")


if __name__ == "__main__":
    main()
