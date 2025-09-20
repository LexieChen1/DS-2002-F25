.PHONY: all fetch analyze clean

# Default target 
analyze: fetch
	./analyze_data.sh

fetch: 
	./fetch_metars.sh

clean: 
	rm -rf raw_metars weather_report.csv
