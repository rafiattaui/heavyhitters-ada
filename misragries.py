def misra_gries(k: int, stream: list) -> dict:
    """
    Implements the Misra-Gries algorithm to find all elements in a stream
    that occur more than n/k times.

    Parameters:
    k (int): The threshold divisor.
    stream (list): The input stream of elements.

    Returns:
    dict: A dictionary with elements as keys and their estimated counts as values.
    """
    if k < 2:
        raise ValueError("k must be at least 2")

    # Step 1: Initialize an empty dictionary to hold candidate elements and their counts
    candidates = {}

    # Step 2: Process each element in the stream
    for element in stream:
        if element in candidates:
            candidates[element] += 1
        elif len(candidates) < k - 1:
            candidates[element] = 1
        else:
            # Decrease count of all candidates
            for key in list(candidates.keys()):
                candidates[key] -= 1
                if candidates[key] == 0:
                    del candidates[key]

    # Step 3: Verify the counts of the candidates
    final_counts = {key: 0 for key in candidates.keys()}
    for element in stream:
        if element in final_counts:
            final_counts[element] += 1

    # Step 4: Filter out elements that occur more than n/k times
    n = len(stream)
    result = {key: count for key, count in final_counts.items() if count > n / k}

    return result

if __name__ == "__main__":
    pass