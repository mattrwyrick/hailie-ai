
import json
import datetime
import requests

import pandas as pd

from hailie.settings import OLLAMA_URL, OLLAMA_MODEL_NAME, DOCS_CATEGORIES, SUMMARY_PATH


MAX_CHAR_LENGTH = 3500
CONTEXT_1 = "Your name is Hailie. You are a senior quant and technologist at a top hedge fund in Chicago with expertise in derivatives, financial modeling, blockchain systems, statistics, and machine learning. Write with the precision of a research analyst, emphasizing mathematical intuition, model structure, and risk implications for a technically proficient audience."


def assign_category(text, file_name=None, categories=DOCS_CATEGORIES,  instruction=None, context=None):
    """
    Assign a category to the given file
    :param text:
    :param file_name:
    :param categories:
    :param instruction:
    :param context:
    :return:
    """
    category_text = ", ".join(categories)
    if instruction is None:
        if file_name is None:
            instruction = f"Review the given text and assign it one of these categories ({category_text}). Only output the category name."
        else:
            instruction = f"Review the given text (for file {file_name}) and assign it one of these categories ({category_text}). Only output the category name."
    if context is None:
        context = CONTEXT_1

    category = invoke_ollama(text, instruction, context)
    category = category.lower().strip().replace(".", "")
    if category not in categories:
        return "misc"
    return category


def create_alt_file_name(text, file_name, instruction=None, context=None):
    """
    Get an alternative / updated file name
    :param text:
    :param file_name:
    :param instruction:
    :param context:
    :return:
    """
    ext = file_name.split(".")[-1].lower().strip()
    if instruction is None:
        if file_name is None:
            instruction = "Create a file name based on the text. Only output the file name:"
        else:
            instruction = f"Create a new file name (currently {file_name}) based on the text. Only output the file name:"
    if context is None:
        context = CONTEXT_1

    alt_file_name = invoke_ollama(text, instruction, context)
    alt_ext = alt_file_name.split(".")[-1].lower().strip()
    if alt_ext != ext:
        if f".{ext}" in alt_file_name:
            alt_file_name = alt_file_name.split(f".{ext}")[0] + f".{ext}"
        else:
            alt_file_name += ext
    return alt_file_name


def create_summary(text, instruction=None, context=None):
    """
    Summarize the given text
    :param text:
    :param instruction:
    :param context:
    :return:
    """
    if instruction is None:
        instruction = "Summarize the text in 5-30 sentences based on complexity.:"
    if context is None:
        context = CONTEXT_1

    summary = invoke_ollama(text, instruction, context)
    if "\n\n" in summary:
        parts = summary.split("\n\n")
        if len(parts) > 1:
            summary = "".join(parts[1:])
    return summary


def add_summary_entry(text, file_name, category):
    """
    Add the summary to the csv
    :param text:
    :param file_name:
    :param category:
    :return:
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    summary_df = pd.read_csv(SUMMARY_PATH)
    row = {
        "File Name": file_name,
        "Category": category,
        "Date [Added]": date,
        "Date [Last Modified]": date,
        "Summary": text
    }
    row_df = pd.DataFrame([row])
    summary_df = pd.concat([summary_df, row_df], ignore_index=True)
    summary_df.to_csv(SUMMARY_PATH, index=False)
    return True


def lookup_summary_entry(*args, **kwargs):
    """
    Get the summary entry for a given file
    :param args:
    :param kwargs:
    :return:
    """
    pass


def invoke_ollama(text, instruction, context=CONTEXT_1):
    """
    Provide a summary of the text
    :param text:
    :param instruction:
    :param context:
    :return:
    """
    char_count = len(instruction)
    char_count += len(context)
    char_left = MAX_CHAR_LENGTH - char_count
    trim_index = min(len(text), char_left)
    trim_text = text[:trim_index]
    prompt = f"{instruction} {trim_text}"

    body = {
        "model": OLLAMA_MODEL_NAME,
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OLLAMA_URL, json=body)
    raw_content = response.content.decode().strip()
    string_parts = [string for string in raw_content.split("\n")]
    parts = list()
    for string in string_parts:
        try:
            json_obj = json.loads(string)
            part = json_obj["message"]["content"]
            parts.append(part)
        except Exception as e:
            pass
    result = "".join(parts)
    return result

