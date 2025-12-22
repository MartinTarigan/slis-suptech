def normalize_and_compare(val1: str, val2: str) -> int:
    """
    Utility sederhana: bandingkan dua string (case-insensitive).
    Return:
    - 100 jika sama
    - 0 jika beda/ada yang kosong
    """
    if not isinstance(val1, str) or not isinstance(val2, str) or not val1 or not val2:
        return 0
    return 100 if val1.strip().lower() == val2.strip().lower() else 0
