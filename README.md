# Amazon Product Price Tracker (V1)

A Python-based Amazon price tracker built with Playwright that allows users to:

- Track multiple Amazon products
- Store product price history in CSV format
- Detect duplicate products automatically
- Compare current prices with previously recorded prices
- Save all scraped data locally for future analysis

This project was built as a learning project to practice:
- Web Scraping
- Browser Automation
- Data Persistence
- File Handling
- Error Handling
- Python Project Structure

---

## Features

### Add New Products

Enter Amazon product URLs and the tracker will:

- Clean unnecessary URL parameters
- Store unique product URLs in `products.txt`
- Scrape product title and current price
- Save results to `prices.csv`

### Duplicate Product Detection

If a product already exists in `products.txt`:

- The URL is not stored again
- The tracker automatically performs a price comparison

### Price Comparison

For previously tracked products, the tracker displays:

- Current price
- Previous recorded price
- Price increase amount
- Price decrease amount
- No-change notification

### Historical Price Storage

Every scrape is recorded in:

```csv
timestamp,url,product_title,price
```

allowing future price history analysis.

---

## Tech Stack

- Python 3
- Playwright
- Pandas
- CSV
- Pathlib

---

## Project Structure

```text
product-price-tracker/
│
├── src/
│   └── tracker.py
│
├── data/
│   ├── products.txt
│   └── prices.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/product-price-tracker.git
cd product-price-tracker
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright Browser

```bash
playwright install
```

---

## Usage

Run:

```bash
python src/tracker.py
```

Example:

```text
Enter number of products: 2

Enter the urls:
https://amazon.in/product1
https://amazon.in/product2
```

---

## Example Output

### Duplicate Product Comparison

```text
==================================================
PRODUCT COMPARISON

Title: IT (REISSUES)

Current price: ₹546
Previous price: ₹546

No change in product price.
==================================================
```

### New Product Tracking

```text
==================================================
PRODUCT 1:

Title: PET SEMATARY (REISSUE)

Price: ₹522
==================================================
```

---

## Sample Data Files

### products.txt

```text
https://www.amazon.in/Stephen-King/dp/1444707868/
https://www.amazon.in/Shining-Stephen-King/dp/1444720724/
https://www.amazon.in/IF-IT-BLEEDS-B-PB/dp/1529391571/
https://www.amazon.in/Dark-Tower-IV-Wizard-Glass/dp/1444723472/
https://www.amazon.in/Stand-Stephen-King/dp/1444720732/
https://www.amazon.in/Pet-Sematary-Stephen-King/dp/1444708139/
```

### prices.csv

```csv
18-06-26 13:26:17,https://www.amazon.in/Stephen-King/dp/1444707868/,IT (REISSUES),546
18-06-26 13:26:19,https://www.amazon.in/Pet-Sematary-Stephen-King/dp/1444708139/,PET SEMATARY (REISSUE),522
```

---

## Error Handling

Implemented handling for:

- Invalid numeric input
- Invalid Amazon URLs
- Missing `products.txt`
- Empty `prices.csv`
- Scraping failures
- Unexpected runtime exceptions

This prevents the program from crashing when invalid data is entered.

---

## Future Improvements (V2)

Planned upgrades:

- Email price alerts
- Scheduled tracking
- SQLite database integration
- Product dashboard
- Price history visualization
- Multi-site support
- FastAPI backend
- React frontend
- Full-stack deployment

---

## What I Learned

During this project I practiced:

- Web scraping with Playwright
- Browser automation
- Working with CSV files
- Data analysis using Pandas
- Error handling in Python
- Relative file paths using Pathlib
- Project organization
- Git and GitHub workflows

---

## Disclaimer

This project is intended for educational purposes only.

Amazon may change its website structure at any time, which can break scraping logic. Always review and comply with the target website's Terms of Service before scraping.

---

## Author

Built by Rohan Nagarajan as part of a Software Engineering and Web Scraping learning journey.