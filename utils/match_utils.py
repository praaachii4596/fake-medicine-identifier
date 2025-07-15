from rapidfuzz import fuzz
import pandas as pd

def load_medicine_dataframe(file='data/cleaned_who_data.csv'):
    """
    Load cleaned WHO medicine list into a DataFrame.
    """
    return pd.read_csv(file)

def fuzzy_match(input_name, df, base_threshold=75):
    """
    Match input_name against WHO medicine aliases using fuzzy logic.
    Returns top 5 matches with scores.

    Scoring logic:
    - Uses ratio, token set ratio, partial ratio
    - Adds boost if input is substring of alias
    - Lowers threshold for short inputs
    """
    input_name = input_name.lower()
    matches = []

    for _, row in df.iterrows():
        # Evaluate alias list safely
        alias_list = eval(row['match_aliases']) if isinstance(row['match_aliases'], str) else row['match_aliases']
        best_score = 0

        for alias in alias_list:
            score_ratio = fuzz.ratio(input_name, alias)
            score_partial = fuzz.partial_ratio(input_name, alias)
            score_token = fuzz.token_set_ratio(input_name, alias)

            substring_boost = 10 if input_name in alias else 0
            final_score = (0.4 * score_ratio + 0.4 * score_token + 0.2 * score_partial) + substring_boost
            best_score = max(best_score, final_score)

        # Use lower threshold for short inputs (e.g., "bcg")
        dynamic_threshold = base_threshold if len(input_name) > 4 else 60

        if best_score >= dynamic_threshold:
            matches.append((row, round(best_score)))

    # Sort by highest score
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:5]