#!/usr/bin/env python3
import os
import pandas as pd
import json
import sys

#grab json lookup files and turn into clean dataframe
def _load_lookup_data(lookup_dir):
    """Load and clean all card lookup json files"""
    all_lookup_df = []

    for file in os.listdir(lookup_dir):
        if file.endswith(".json"):
            filepath = os.path.join(lookup_dir, file)
            with open(filepath, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON file: {filepath}", file=sys.stderr)
                    continue

            df = pd.json_normalize(data["data"])
            holofoil = df.get("tcgplayer.prices.holofoil.market", pd.Series([0.0] * len(df)))
            normal = df.get("tcgplayer.prices.normal.market", pd.Series([0.0] * len(df)))

            df["card_market_value"] = holofoil.fillna(normal).fillna(0.0)


            df = df.rename(columns={
                "id": "card_id",
                "name": "card_name",
                "number": "card_number",
                "set.id": "set_id",
                "set.name": "set_name"
            })

            required_cols = [
                "card_id", "card_name", "card_number",
                "set_id", "set_name", "card_market_value"
            ]
            df = df[[col for col in required_cols if col in df.columns]]
            all_lookup_df.append(df)

    if not all_lookup_df:
        return pd.DataFrame()

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    lookup_df = lookup_df.sort_values("card_market_value", ascending=False)
    lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first")

    return lookup_df


def _load_inventory_data(inventory_dir):
    """Load and merge all inventory CSV files"""
    inventory_data = []

    for file in os.listdir(inventory_dir):
        if file.endswith(".csv"):
            filepath = os.path.join(inventory_dir, file)
            df = pd.read_csv(filepath)
            inventory_data.append(df)

    if not inventory_data:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data, ignore_index=True)
    inventory_df["card_id"] = (
        inventory_df["set_id"].astype(str)
        + "-"
        + inventory_df["card_number"].astype(str)
    )

    return inventory_df


def update_portfolio(inventory_dir, lookup_dir, output_file):
    """Main ETL pipeline: merge lookup + inventory and export portfolio"""
    inventory_df = _load_inventory_data(inventory_dir)
    lookup_df = _load_lookup_data(lookup_dir)

    if inventory_df.empty:
        print("Error: No inventory data found.", file=sys.stderr)
        empty_cols = [
            "card_name", "set_id", "card_number",
            "binder_name", "page_number", "slot_number"
        ]
        pd.DataFrame(columns=empty_cols).to_csv(output_file, index=False)
        return

    merged_df = pd.merge(inventory_df, lookup_df, on="card_id", how="left")
    merged_df["card_market_value"] = merged_df["card_market_value"].fillna(0.0)
    merged_df["set_name"] = merged_df["set_name"].fillna("NOT_FOUND")

    if {"binder_name", "page_number", "slot_number"}.issubset(merged_df.columns):
        merged_df["index"] = (
            merged_df["binder_name"].astype(str)
            + "-"
            + merged_df["page_number"].astype(str)
            + "-"
            + merged_df["slot_number"].astype(str)
        )

    merged_df.rename(columns={
        "name": "card_name",
        "number": "card_number",
        "set.id": "set_id",
        "set.name": "set_name"
    }, inplace=True)
    
    for base in ["card_name", "card_number", "set_id"]:
        if f"{base}_x" in merged_df.columns:
            merged_df[base] = merged_df[f"{base}_x"]
        elif f"{base}_y" in merged_df.columns:
            merged_df[base] = merged_df[f"{base}_y"]
    
    final_cols = [
        "card_id", "card_name", "card_number",
        "set_id", "set_name", "card_market_value",
        "binder_name", "page_number", "slot_number"
    ]
    if "index" in merged_df.columns:
        final_cols.append("index")

    existing_cols = [col for col in final_cols if col in merged_df.columns]
    missing_cols = [col for col in final_cols if col not in merged_df.columns]

    if missing_cols:
        print(f"Warning: Missing columns from merged data: {missing_cols}", file=sys.stderr)

    merged_df[existing_cols].to_csv(output_file, index=False)
    print(f"Portfolio successfully saved to {output_file}")


def main():
    """Production run"""
    update_portfolio("./card_inventory", "./card_set_lookup", "card_portfolio.csv")

def test():
    """Test run"""
    update_portfolio("./card_inventory_test", "./card_set_lookup_test", "test_card_portfolio.csv")

if __name__ == "__main__":
    print("Running update_portfolio.py in TEST mode...", file=sys.stderr)
    test()