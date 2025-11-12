
import os
import json
import shutil


from hailie.settings import (
    DOCS_DIR,
    DOCS_SUMMARY_PATH,

    DOCS_BLOCKCHAIN_QUEUE_DIR,
    DOCS_BLOCKCHAIN_COMPLETED_DIR,
    DOCS_BLOCKCHAIN_REFERENCE_DIR,

    DOCS_FINANCE_QUEUE_DIR,
    DOCS_FINANCE_COMPLETED_DIR,
    DOCS_FINANCE_REFERENCE_DIR,

    DOCS_MACHINE_LEARNING_QUEUE_DIR,
    DOCS_MACHINE_LEARNING_COMPLETED_DIR,
    DOCS_MACHINE_LEARNING_REFERENCE_DIR,

    DOCS_STATISTICS_QUEUE_DIR,
    DOCS_STATISTICS_REFERENCE_DIR,
    DOCS_STATISTICS_COMPLETED_DIR,

    DOCS_MISC_QUEUE_DIR,
    DOCS_MISC_COMPLETED_DIR,
    DOCS_MISC_REFERENCE_DIR
)


DIR_MAP = {
    "blockchain": {
        "queue": DOCS_BLOCKCHAIN_QUEUE_DIR,
        "completed": DOCS_BLOCKCHAIN_COMPLETED_DIR,
        "reference": DOCS_BLOCKCHAIN_REFERENCE_DIR
    },
    "finance": {
        "queue": DOCS_FINANCE_QUEUE_DIR,
        "completed": DOCS_FINANCE_COMPLETED_DIR,
        "reference": DOCS_FINANCE_REFERENCE_DIR
    },
    "machine_learning": {
        "queue": DOCS_MACHINE_LEARNING_QUEUE_DIR,
        "completed": DOCS_MACHINE_LEARNING_COMPLETED_DIR,
        "reference": DOCS_MACHINE_LEARNING_REFERENCE_DIR
    },
    "statistics": {
        "queue": DOCS_STATISTICS_QUEUE_DIR,
        "completed": DOCS_STATISTICS_COMPLETED_DIR,
        "reference": DOCS_STATISTICS_REFERENCE_DIR
    },
    "misc": {
        "queue": DOCS_MISC_QUEUE_DIR,
        "completed": DOCS_MISC_COMPLETED_DIR,
        "reference": DOCS_MISC_REFERENCE_DIR
    }
}


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
