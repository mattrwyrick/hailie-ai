
import os
import shutil

from hailie.management import DIR_MAP


def move_file_to_completed(file_name, category):
    """
    Move the given file to the completed folder
    :param file_name:
    :param category:
    :return:
    """
    category = category.strip().lower()
    if category in DIR_MAP:
        reference_dir = DIR_MAP[category]["reference"]
        tgt_path = str(os.path.join(reference_dir, file_name))

        queue_dir = DIR_MAP[category]["queue"]
        files = os.listdir(queue_dir)
        if file_name in files:
            src_path = str(os.path.join(queue_dir, file_name))
            if os.path.isfile(src_path):
                shutil.move(src_path, tgt_path)
                return True
            raise Exception(f"Error in making src_path. {src_path} is not a file.")

    return False


def move_file_to_reference(file_name, category):
    """
    Move the given file to the reference folder
    :param file_name:
    :param category:
    :return:
    """
    category = category.strip().lower()
    if category in DIR_MAP:
        reference_dir = DIR_MAP[category]["reference"]
        tgt_path = str(os.path.join(reference_dir, file_name))

        queue_dir = DIR_MAP[category]["queue"]
        files = os.listdir(queue_dir)
        if file_name in files:
            src_path = str(os.path.join(queue_dir, file_name))
            if os.path.isfile(src_path):
                shutil.move(src_path, tgt_path)
                return True
            raise Exception(f"Error in making src_path. {src_path} is not a file.")

        completed_dir = DIR_MAP[category]["completed"]
        files = os.listdir(completed_dir)
        if file_name in files:
            src_path = str(os.path.join(queue_dir, file_name))
            if os.path.isfile(src_path):
                shutil.move(src_path, tgt_path)
                return True
            raise Exception(f"Error in making src_path. {src_path} is not a file.")

    return False
