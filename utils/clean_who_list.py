import pandas as pd
import re

def extract_aliases(name):
    """
    Generate possible matching aliases for a medicine name:
    - Original lowercase name
    - Name with special characters removed
    - Words inside parentheses
    - Parts split by commas
    """
    name = str(name).lower()
    aliases = set()

    aliases.add(name)

    # Remove symbols and split
    clean = re.sub(r'[+()\\[\],/]', ' ', name)
    clean = re.sub(r'\s+', ' ', clean)
    aliases.update(clean.strip().split())

    # Add text inside parentheses
    paren_matches = re.findall(r'\((.*?)\)', name)
    for pm in paren_matches:
        aliases.add(pm.strip())

    # Add parts split by comma
    if ',' in name:
        for part in name.split(','):
            aliases.add(part.strip())

    return list(aliases)

def clean_for_matching(text):
    """
    Remove unwanted characters and extra spaces for fuzzy matching.
    """
    text = re.sub(r'[+,()\\[\]/]', ' ', str(text).lower())
    return re.sub(r'\s+', ' ', text).strip()

def clean_who_list(input_file='data/who_essential_meds_2023.csv',
                   output_file='data/cleaned_who_data.csv'):
    """
    Load and clean WHO medicine list:
    - Removes entries marked as 'removed'
    - Generates 'clean_name' and alias list for fuzzy matching
    - Saves cleaned result as a CSV
    """
    df = pd.read_csv(input_file)

    # Exclude removed medicines
    if 'Status' in df.columns:
        df = df[df['Status'].str.lower() != 'removed']

    df['clean_name'] = df['Medicine name'].apply(clean_for_matching)
    df['match_aliases'] = df['Medicine name'].apply(extract_aliases)

    # Drop rows with missing names
    df = df.dropna(subset=['clean_name'])

    df.to_csv(output_file, index=False)
    print(f"✅ Cleaned data saved to: {output_file}")

if __name__ == "__main__":
    clean_who_list()