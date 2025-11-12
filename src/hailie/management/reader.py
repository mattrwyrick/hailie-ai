
import os

from pypdf import PdfReader


def get_content_from_pdf(file_path):
    """
    Return the text of a given pdf file
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path) and file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        page_texts = list()
        for page in reader.pages:
            text = page.extract_text()
            page_texts.append(text)
        text = "\n".join(page_texts)
        return text
    return None


def get_content_from_file(file_path, encoding="utf-8"):
    """
    Return the text of a given txt file
    :param file_path:
    :param encoding:
    :return:
    """
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding=encoding) as f:
            text = f.read()
        return text
    return None

