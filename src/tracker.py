from playwright.sync_api import sync_playwright
import csv
from datetime import datetime
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

PRICE_FILE = BASE_DIR / "data" / "prices.csv"
PRODUCT_FILE = BASE_DIR / "data" / "products.txt"

urls = []
comp_urls = []


def get_urls():
    try:
        url_no = int(input("Enter number of products: "))
    except ValueError:
        print("Enter a valid number.")
        return
    url_count = url_no
    try:
        with open(PRODUCT_FILE, 'r', encoding="utf-8") as products_file:
            all_urls = {
                line.strip()
                for line in products_file
            }
            print("Enter the urls:")
            for i in range(0, url_count):
                url = input()
                url = clean_url(url)
                if url is None:
                    print("Invalid Amazon url.")
                    continue
                if url in all_urls:
                    print("Duplicate url entered. Comparison will be done....")
                    comp_urls.append(url)
                    continue
                with open(PRODUCT_FILE, 'a', encoding="utf-8") as prod_write_file:
                    prod_write_file.write(f"{url}\n")
                    urls.append(url)
    except FileNotFoundError:
        print("products.txt not found.")
        return


def clean_url(url):
    try:
        str1 = url.split("dp/")
        str2 = str1[1].split("/")[0] + "/"
        product_url = str1[0] + "dp/" + str2
        return product_url
    except IndexError:
        return None


def compare_price(page):
    print("\nFetching product data...")
    try:
        df = pd.read_csv(PRICE_FILE, header=None)
    except pd.errors.EmptyDataError:
        print("Price history file is empty.")
        return
    for url in comp_urls:
        try:
            page.goto(url, wait_until="commit")
            page.locator("#productTitle").wait_for()
            product_title = page.locator("#productTitle").text_content().strip()
            price_symbol = page.locator(".a-price-symbol").first.text_content().strip()
            new_price = price_symbol + page.locator(
                ".a-price-whole").first.text_content().strip()
            int_new_price = int(page.locator(".a-price-whole").first.text_content().strip().replace(",", ""))
            timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
            product_rows = df[df[1] == url]

            product_details = [timestamp, url, product_title, int_new_price]
            save_product(product_details)
            print("="*50)
            print("PRODUCT COMPARISON")
            print("\nTitle: " + product_title)
            print("Current price: " + new_price)
            if not product_rows.empty:
                latest_old_price = product_rows.iloc[-1][3]
                if latest_old_price < int_new_price:
                    print("Previous price: " + price_symbol + str(latest_old_price))
                    print("Price increased by " + price_symbol + str((int_new_price - latest_old_price)))
                elif latest_old_price > int_new_price:
                    print("Previous price: " + price_symbol + str(latest_old_price))
                    print("Price decreased by " + price_symbol + str(abs(int_new_price - latest_old_price)))
                else:
                    print("Previous price: " + price_symbol + str(latest_old_price))
                    print("No change in product price.")
            print("="*50)
        except Exception as e:
            print(f"Failed to scrape {url}")
            print(e)
            continue

def scrape_product(page):
    print("\nFetching product data...")
    count = 1
    for url in urls:
        try:
            page.goto(url, wait_until="commit")
            page.locator("#productTitle").wait_for()
            product_title = page.locator("#productTitle").text_content().strip()
            product_price = page.locator(".a-price-symbol").first.text_content().strip() + page.locator(
                 ".a-price-whole").first.text_content().strip()
            int_price = int(page.locator(".a-price-whole").first.text_content().strip().replace(",", ""))
            timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")

            print("="*50)
            print("PRODUCT " + str(count) + ":")
            print("\nTitle: " + product_title)
            print("Price: " + product_price)
            product_details = [timestamp, url, product_title, int_price]
            save_product(product_details)
            count += 1
        except Exception as e:
            print(f"Failed to scrape {url}")
            print(e)
            continue


def save_product(data):
    with open(PRICE_FILE, 'a', newline="", encoding="utf8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)


def main():
    pw = sync_playwright().start()
    browser = None
    try:
        browser = pw.chromium.launch()
        page = browser.new_page()
        get_urls()
        if comp_urls:
            compare_price(page)
        scrape_product(page)
    finally:
        if browser:
            browser.close()
        pw.stop()


if __name__ == "__main__":
    main()
