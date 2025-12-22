import re
import jellyfish

# Variants nama dari kode Streamlit
NAME_VARIANTS = {
    'mohammad': 'muhammad', 'mohamad': 'muhammad', 'mohamed': 'muhammad',
    'mochammad': 'muhammad', 'mochamad': 'muhammad', 'mahomet': 'muhammad',
    'mehmed': 'muhammad', 'mohammed': 'muhammad', 'moh': 'muhammad',
    'md': 'muhammad', 'abd': 'abdul', 'bin': '', 'binti': ''
}

COMMON_TOKENS = {'muhammad', 'abdul', 'ali', 'ahmad', 'bin', 'binti'}


def normalize_name(name: str) -> str:
    """
    Normalisasi nama:
    - lower
    - hilangkan simbol non alfanumerik
    - mapping varian (NAME_VARIANTS)
    - buang token kosong
    """
    if not isinstance(name, str):
        return ""

    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9\s]', '', name)
    tokens = name.split()

    normalized_tokens = [
        NAME_VARIANTS.get(token, token)
        for token in tokens
        if NAME_VARIANTS.get(token, token)  # buang token yang jadi string kosong (bin/binti)
    ]

    return ' '.join(normalized_tokens)


def calculate_advanced_name_score(
    name1: str,
    name2: str,
    common_token_weight: float = 0.3
) -> float:
    """
    Engine fuzzy name matching dari kode Streamlit:
    - Kombinasi Jaro-Winkler, Levenshtein, dan token-based weighted matching.
    - Output: skor 0–100.
    """
    if not isinstance(name1, str) or not isinstance(name2, str) or not name1 or not name2:
        return 0.0

    norm_name1 = normalize_name(name1)
    norm_name2 = normalize_name(name2)

    if not norm_name1 or not norm_name2:
        return 0.0

    # Global similarity
    jaro_score = jellyfish.jaro_winkler_similarity(norm_name1, norm_name2)
    lev_distance = jellyfish.levenshtein_distance(norm_name1, norm_name2)
    max_len = max(len(norm_name1), len(norm_name2))
    lev_score = (1.0 - (lev_distance / max_len)) if max_len > 0 else 1.0

    # Token-based matching
    tokens1 = sorted(norm_name1.split())
    tokens2 = sorted(norm_name2.split())

    if not tokens1 or not tokens2:
        return ((jaro_score * 0.6) + (lev_score * 0.4)) * 100.0

    temp_tokens2 = list(tokens2)
    total_weight = 0.0
    accumulated_score = 0.0

    for token1 in tokens1:
        best_match_score = 0.0
        best_match_token = None

        for token2 in temp_tokens2:
            jw_score = jellyfish.jaro_winkler_similarity(token1, token2)
            lev_dist = jellyfish.levenshtein_distance(token1, token2)
            max_token_len = max(len(token1), len(token2))
            lev_token_score = (1.0 - (lev_dist / max_token_len)) if max_token_len > 0 else 1.0

            combined_token_score = (jw_score * 0.7) + (lev_token_score * 0.3)

            if combined_token_score > best_match_score:
                best_match_score = combined_token_score
                best_match_token = token2

        weight = common_token_weight if token1 in COMMON_TOKENS else 1.0

        if best_match_token:
            accumulated_score += best_match_score * weight
            temp_tokens2.remove(best_match_token)

        total_weight += weight

    token_set_score = (accumulated_score / total_weight) if total_weight > 0 else 0.0

    final_score = (jaro_score * 0.2) + (lev_score * 0.1) + (token_set_score * 0.7)
    return final_score * 100.0
