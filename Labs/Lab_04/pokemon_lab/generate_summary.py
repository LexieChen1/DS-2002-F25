#!/usr/bin/env 
import os 
import sys
import pandas as pd

def generate_summary(portfolio_file):
    """Read portfolio CSV and print total and most valuable card."""
    if not os.path.exists(portfolio_file):
        print(f"Error: {portfolio_file} not found.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("Portfolio file is empty — no data to summarize.")
        return

    # --- Summary Calculations ---
    total_portfolio_value = df["card_market_value"].sum()
    most_valuable_card = df.loc[df["card_market_value"].idxmax()]

    # --- Reporting Output ---
    print("\n===== Portfolio Summary =====")
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print(
        f"Most Valuable Card: {most_valuable_card['card_name']} "
        f"({most_valuable_card['card_id']}) "
        f"worth ${most_valuable_card['card_market_value']:,.2f}"
    )
    print("==============================\n")


# --- Public Interface Functions ---
def main():
    """Production summary — uses production portfolio file."""
    generate_summary("card_portfolio.csv")


def test():
    """Test summary — uses test portfolio file."""
    generate_summary("test_card_portfolio.csv")


if __name__ == "__main__":
    print("Running generate_summary.py in TEST mode...", file=sys.stderr)
    test()