import pandas as pd
from argparse import ArgumentParser
import json

def get_all_values(df: pd.DataFrame, fields: tuple):
    ls = []
    for i, row in df[list(fields)].iterrows():
        ls.append(tuple(row))
    return tuple(ls)
        
def get_first_values(df: pd.DataFrame, fields: tuple):
    values = []
    for field in fields:
        values.append(df[field].values[0])
    return tuple(values)

def process_outbound_transaction(df: pd.DataFrame, category_map: dict):
    field_names = (
        "Source fee amount",
        "Source amount (after fees)",
        "Source currency",
        "Target amount (after fees)",
        "Target currency"
    )

    rows = get_all_values(df,field_names)

    expense_category = "Expenses:Unassigned"
    source = df["Target name"].values[0]
    if source in category_map:
        expense_category = category_map[source]

    lines = []
    for row in rows:
        source_fee, source_amount, source_currency, target_amount, target_currency = row
        lines.extend([
            f"\tAssets:Wise {-source_amount} {source_currency} @@ {target_amount} {target_currency}",
            f"\t{expense_category} {target_amount} {target_currency}",
        ])
        # currency transfer fees
        if source_currency != target_currency:
            lines.extend([
                f"\tAssets:Wise {-source_fee} {source_currency}",
                f"\tExpenses:Bank-Fees {source_fee} {source_currency}",
        ])
    return lines

def process_neutral_transaction(df: pd.DataFrame, category_map: dict):
    # neutral transfers (balance transfers) are always one line
    field_names = (
        "Source fee amount",
        "Source amount (after fees)",
        "Source currency",
        "Target fee amount",
        "Target amount (after fees)",
        "Target currency"
    )

    source_fee, source_amount, source_currency, target_fee, target_amount, target_currency = get_first_values(df,field_names)

    return [
        f"\tAssets:Wise {-source_amount} {source_currency} @@ {target_amount} {target_currency}",
        f"\tAssets:Wise {target_amount} {target_currency}",
        f"\tAssets:Wise {-source_fee} {source_currency}",
        f"\tExpenses:Bank-Fees {source_fee} {source_currency}",
    ]

def process_inbound_transaction(df: pd.DataFrame, category_map: dict):
    # inbound transactions are easy: they never involve currency transfers
    # they are always one line
    source = df["Source name"].values[0]
    income_account = "Income:Unassigned"
    if source in category_map:
        income_account = category_map[source]

    currency = df["Target currency"].values[0]
    target_amount = df["Target amount (after fees)"].values[0]

    return [
        f"\t{income_account} {-target_amount} {currency}",
        f"\tAssets:Wise {target_amount} {currency}"
    ]

def process_transaction(df: pd.DataFrame, category_map: dict):

    label = ""
    direction = df["Direction"].values[0]
    if direction == "OUT": label = df["Target name"].values[0]
    elif direction == "IN": label = df["Source name"].values[0]
    elif direction == "NEUTRAL": label = "Internal transfer"
    
    bean_head = f"{df['Created on'].values[0][:10]} * \"{label}\""

    lines = []

    if direction == "IN":
        lines = process_inbound_transaction(df, category_map)
    elif direction == "NEUTRAL":
        lines = process_neutral_transaction(df, category_map)
    elif direction == "OUT":
        lines = process_outbound_transaction(df, category_map)

    transaction_str = "\n".join([bean_head] + lines)
    return transaction_str
    
def process(input: str, output: str, category_map: str):
    df = pd.read_csv(input)
    try:
        with open(category_map) as f:
            map = json.load(f)
    except:
        map = {}
    
    grouped = df.groupby("ID")

    out = [ process_transaction(group, map) for name, group in grouped ]

    print('\n\n'.join(out))    

def main():
    parser = ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--map")
    parsed = parser.parse_args()

    args = [vars(parsed)[k] for k in ("input","output","map")]
    process(*args)
    
if __name__ == "__main__":
    main()
