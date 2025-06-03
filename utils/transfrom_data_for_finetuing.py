import json


def split_dataset(dataset):
    """
    Split a dataset into separate question and CoT datasets.

    Args:
        dataset (list): List of dictionaries containing puzzle data

    Returns:
        tuple: (question_dataset, cot_dataset) - two lists of dictionaries
    """
    question_dataset = []
    cot_dataset = []

    for item in dataset:
        # Create question entry
        question_entry = {
            "question": item["question"],
            "question_parsing": item["question_parsing"],
            "id": item["id"],
            "sel_idx": item["sel_idx"]
        }
        question_dataset.append(question_entry)

        # Create CoT entry
        cot_entry = {
            "answer": item["answer"],
            "id": item["id"],
            "cot": item["cot"],
            "cot_parsing": item["cot_parsing"],
            "sel_idx": item["sel_idx"]
        }
        cot_dataset.append(cot_entry)

    return question_dataset, cot_dataset


def format_qp_for_openpipe_finetuning(question_dataset, system_prompt):
    """
    Format split datasets into OpenPipe fine-tuning format (which follows OpenAI's format).

    Args:
        question_dataset: List of question dictionaries
        cot_dataset: List of corresponding CoT dictionaries

    Returns:
        list: List of formatted examples ready for OpenPipe fine-tuning
    """
    formatted_data = []

    for q_item in question_dataset:
        # Create the formatted example
        example = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": q_item["question"]
                },
                {
                    "role": "assistant",
                    "content": q_item["question_parsing"]
                }
            ]
        }
        formatted_data.append(example)

    return formatted_data


def format_cp_for_openpipe_finetuning(cot_dataset, system_prompt):
    """
    Format CoT datasets for OpenPipe/OpenAI fine-tuning to generate cot_parsing.

    Args:
        cot_dataset: List of CoT dictionaries containing answer, cot, cot_parsing fields

    Returns:
        list: List of formatted examples ready for fine-tuning
    """
    formatted_data = []

    for item in cot_dataset:
        cot_parsing = item.pop('cot_parsing')
        # Create the formatted example
        example = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(item)
                },
                {
                    "role": "assistant",
                    "content": json.dumps(cot_parsing, indent=2)
                }
            ]
        }
        formatted_data.append(example)

    return formatted_data
