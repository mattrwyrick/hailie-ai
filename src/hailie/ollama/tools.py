

import requests

from hailie.settings import OLLAMA_URL, OLLAMA_MODEL_NAME


MAX_CHAR_LENGTH = 1000
CONTEXT_1 = "Your name is Hailie. You are a senior quant and technologist at a top hedge fund in Chicago with expertise in derivatives, financial modeling, blockchain systems, statistics, and machine learning. Write with the precision of a research analyst, emphasizing mathematical intuition, model structure, and risk implications for a technically proficient audience."


def create_alt_file_name(text, file_name, instruction=None, context=None):
    """
    Summarize the given text
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
        instruction = "Summarize the text:"
    if context is None:
        context = CONTEXT_1

    summary = invoke_ollama(text, instruction, context)
    return summary


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
    content = response.json()

    return content

