
import os
import logging
import shutil

import pandas as pd

from hailie.settings import DOCS_DUMP_DIR, DOCS_CATEGORIES
from hailie.management import DIR_MAP
from hailie.management.reader import get_content_from_pdf, get_content_from_file
from hailie.ollama.tools import create_alt_file_name, assign_category, create_summary, add_summary_entry
from hailie.rag.tools import create_embedding, add_embedding_entry


def move_dump_file_to_queue(file_name, category=None, rename=True, add_embedding=True, add_summary=True):
    """
    Move the file in dump to queue
    :return:
    """
    status = False
    file_name = file_name.strip()
    dump_file_path = str(os.path.join(DOCS_DUMP_DIR, file_name))

    if not os.path.isfile(dump_file_path):
        return status, file_name, category

    if dump_file_path.lower().endswith(".pdf"):
        content = get_content_from_pdf(dump_file_path)
    else:
        content = get_content_from_file(dump_file_path)

    if rename:
        alt_file_name = create_alt_file_name(content, file_name)
    else:
        alt_file_name = file_name

    if category is None or category not in DOCS_CATEGORIES:
        category = assign_category(content, alt_file_name)


    status = True

    if add_embedding:
        vector = create_embedding(content, alt_file_name, category)
        embedding_status = add_embedding_entry(vector, alt_file_name, category)
        status = embedding_status and status

    if add_summary:
        summary = create_summary(content)
        summary_status = add_summary_entry(summary, alt_file_name, category)
        status = summary_status and status

    queue_dir = DIR_MAP[category]["queue"]
    queue_file_path = str(os.path.join(queue_dir, alt_file_name))
    shutil.move(dump_file_path, queue_file_path)

    return status, alt_file_name, category


def move_dump_files_to_queue(rename=True, add_embedding=True, add_summary=True):
    """
    Move dump files to their queue category
    :param rename:
    :param add_embedding:
    :param add_summary:
    :return:
    """
    file_names = [file_name for file_name in os.listdir(DOCS_DUMP_DIR)]
    successes = list()
    for file_name in file_names:
        status, alt_file_name, category = move_dump_file_to_queue(
            file_name,
            rename=rename,
            add_embedding=add_embedding,
            add_summary=add_summary
        )
        value = [status, file_name, alt_file_name, category]
        successes.append(value)

    return successes