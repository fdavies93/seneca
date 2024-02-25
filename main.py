import pandas as pd
from argparse import ArgumentParser

def process_transaction(df: pd.DataFrame):

    label = ""
    if df["Direction"].values[0] == "OUT": label = df["Target name"].values[0]
    elif df["Direction"].values[0] == "IN": label = df["Source name"].values[0]
    elif df["Direction"].values[0] == "NEUTRAL": label = "Internal transfer"
    
    bean_head = f"{df['Created on'].values[0][:10]} * \"{label}\""
    print(bean_head)
    print(df)

def process(input: str, output: str, shortcuts: str):
    df = pd.read_csv(input)
    grouped = df.groupby("ID")
    for name, group in grouped:
        bean_count = process_transaction(group)

def main():
    parser = ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--shortcuts")
    parsed = parser.parse_args()

    args = [vars(parsed)[k] for k in ("input","output","shortcuts")]
    process(*args)
    
if __name__ == "__main__":
    main()
