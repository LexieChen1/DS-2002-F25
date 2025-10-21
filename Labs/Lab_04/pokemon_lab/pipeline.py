import sys
import generate_summary
import update_portfolio

def run_production_pipeline():
    print("Starting pipeline...", file=sys.stderr)
    print("Running ETL update...", file=sys.stdout)

    update_portfolio.main()
    print("Generating report...", file=sys.stdout)

    generate_summary.main()
    print("Pipeline completed successfully!", file=sys.stderr)


if __name__ == "__main__":
    run_production_pipeline()