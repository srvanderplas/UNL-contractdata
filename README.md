# UNL Contracts

## Data Source

Data were scraped from https://statecontracts.nebraska.gov/ with the following search parameters:

- Status: Active
- Type: Higher Education
- Entity: University of Nebraska Lincoln
- DocType: Contract
- Amount: Any

## Files

### Data

- `Scraped_Contracts.csv` - Data in raw form from the website
- `Cleaned_Contracts.csv` - Dates and dollar amounts cleaned up and formatted as canonical data types
- `Vendor_Summary.csv` - Vendor-by-vendor total contract amounts

### Code

- `Scrape.py` - Scrape data from the website using the python package `mechanize` and `pandas` for data wrangling
- `Clean_Data.R` - R script to work with the data and convert column formats to reasonable data types. Generates `Cleaned_Contracts.csv` and `Vendor_Summary.csv`

## License

CC-By-4.0 no attribution necessary.
