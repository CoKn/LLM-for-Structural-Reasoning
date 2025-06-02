def find_similar_items(items, keys_to_compare=None, threshold=0.8):
    """
    Find potential similar items using Levenshtein distance on specified keys.

    Args:
        items (list): List of dictionaries
        keys_to_compare (str or list): Key(s) to compare. If None, compares whole dictionaries.
        threshold (float): Similarity threshold (0-1) where 1 means identical

    Returns:
        list: List of tuples containing (item_id_1, item_id_2, similarity) for potential duplicates
    """

    def levenshtein_distance(s1, s2):
        """Calculate the Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def get_comparison_text(item, keys):
        """Extract text to compare from item based on keys."""
        if keys is None:
            return str(item)

        if isinstance(keys, str):
            keys = [keys]

        # Concatenate values from all specified keys
        return " ".join(str(item.get(k, "")) for k in keys if k in item)

    potential_duplicates = []

    # Compare each item with all others
    for i in range(len(items)):
        text1 = get_comparison_text(items[i], keys_to_compare)

        for j in range(i + 1, len(items)):
            text2 = get_comparison_text(items[j], keys_to_compare)

            # Skip empty comparisons
            if not text1 or not text2:
                continue

            # Calculate Levenshtein distance
            distance = levenshtein_distance(text1, text2)

            # Normalize the distance to get similarity (0-1)
            max_len = max(len(text1), len(text2))
            similarity = 1 - (distance / max_len) if max_len > 0 else 1

            # If similarity is above threshold, consider it a potential duplicate
            if similarity >= threshold:
                id1 = items[i].get('id', i)
                id2 = items[j].get('id', j)
                potential_duplicates.append((id1, id2, similarity))

    return potential_duplicates