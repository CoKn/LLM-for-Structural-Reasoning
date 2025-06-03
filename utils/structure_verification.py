def verify_gpt_item_structure(item):
    """
    Verify that a single dictionary has the required structure:
      {
        "question": <str>,
        "question_parsing": <list of str>,
        "answer": <str>,
        "cot": <str>,
        "cot_parsing": <list of dict>,
        "id": <int>,
        "sel_idx": <int>
      }
    and that within cot_parsing, each dict has exactly the keys:
      "statement": <str>,
      "evidence": <str>,
      "Verification": <str>
    Returns a list of error messages (empty if no errors).
    """
    errors = []

    # 1) Top‐level keys
    required_top_keys = {"question", "question_parsing", "answer", "cot", "cot_parsing", "id", "sel_idx"}
    missing = required_top_keys - set(item.keys())
    extra = set(item.keys()) - required_top_keys
    if missing:
        errors.append(f"Missing keys at top level: {missing}")
    if extra:
        errors.append(f"Unexpected extra keys at top level: {extra}")

    # 2) "question" must be a string
    if "question" in item and not isinstance(item["question"], str):
        errors.append(f'"question" should be a str, got {type(item["question"]).__name__!r}')

    # 3) "question_parsing" must be a list of strings
    if "question_parsing" in item:
        qp = item["question_parsing"]
        if not isinstance(qp, list):
            errors.append(f'"question_parsing" should be a list, got {type(qp).__name__!r}')
        else:
            for idx, entry in enumerate(qp):
                if not isinstance(entry, str):
                    errors.append(f'  question_parsing[{idx}] should be a str, got {type(entry).__name__!r}')

    # 4) "answer" must be a string
    if "answer" in item and not isinstance(item["answer"], str):
        errors.append(f'"answer" should be a str, got {type(item["answer"]).__name__!r}')

    # 5) "cot" must be a string
    if "cot" in item and not isinstance(item["cot"], str):
        errors.append(f'"cot" should be a str, got {type(item["cot"]).__name__!r}')

    # 6) "cot_parsing" must be a list of dicts with keys "statement", "evidence", "Verification"
    if "cot_parsing" in item:
        cp = item["cot_parsing"]
        if not isinstance(cp, list):
            errors.append(f'"cot_parsing" should be a list, got {type(cp).__name__!r}')
        else:
            for idx, d in enumerate(cp):
                if not isinstance(d, dict):
                    errors.append(f'  cot_parsing[{idx}] should be a dict, got {type(d).__name__!r}')
                    continue

                required_inner = {"statement", "evidence", "Verification"}
                missing_inner = required_inner - set(d.keys())
                extra_inner = set(d.keys()) - required_inner
                if missing_inner:
                    errors.append(f'  cot_parsing[{idx}] missing keys: {missing_inner}')
                if extra_inner:
                    errors.append(f'  cot_parsing[{idx}] has unexpected keys: {extra_inner}')

                # check types of inner values
                for key in required_inner & set(d.keys()):
                    if not isinstance(d[key], str) and not isinstance(d[key], bool):
                        errors.append(f'  cot_parsing[{idx}]["{key}"] should be str, got {type(d[key]).__name__!r}')

    # 7) "id" and "sel_idx" must be integers
    for int_key in ("id", "sel_idx"):
        if int_key in item and not isinstance(item[int_key], int):
            errors.append(f'"{int_key}" should be an int, got {type(item[int_key]).__name__!r}')

    return errors


def verify_all_gpt_items(data_list):
    """
    Iterate over a list of dictionaries and verify each one against the required structure.
    Returns a tuple (bad_entries, good_indices):
      - bad_entries: list of (index, errors) for any items that failed.
      - good_indices: list of indices for items that passed validation.
    Also prints how many entries are wrongly formatted.
    """
    bad_entries = []
    good_indices = []

    for idx, item in enumerate(data_list):
        errs = verify_gpt_item_structure(item)
        if errs:
            bad_entries.append((idx, errs))
        else:
            good_indices.append(idx)

    # Print how many entries failed validation
    print(f"Found {len(bad_entries)} wrongly formatted entr{'y' if len(bad_entries)==1 else 'ies'}.")

    return bad_entries, good_indices


