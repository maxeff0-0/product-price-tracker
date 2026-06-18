from playwright.sync_api import sync_playwright
import csv
from datetime import datetime
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

PRICE_FILE = BASE_DIR/"data"/"prices.csv"
PRODUCT_FILE = BASE_DIR/"data"/"products.txt"

urls = []
comp_urls = []

def get_urls():
     url_no = int(input("Enter number of products: "))
     url_count = url_no
     with open(PRODUCT_FILE, 'r', encoding="utf-8") as products_file:
          all_urls = {
               line.strip()
               for line in products_file
          }
          print("Enter the urls:")
          for i in range(0, url_count):
              url = input()
              url = clean_url(url)
              if url in all_urls:
                  print("Duplicate url entered. Comparison will be done....")
                  comp_urls.append(url)
                  continue
              with open(PRODUCT_FILE, 'a', encoding="utf-8") as prod_write_file:
                  prod_write_file.write(f"{url}\n")
                  urls.append(url)

def clean_url(url):
     str1 = url.split("dp/")
     str2 = str1[1].split("/")[0] + "/"
     product_url = str1[0] + "dp/" + str2
     return product_url

def compare_price(page):
     df = pd.read_csv(PRICE_FILE, header=None)
     for url in comp_urls:
          page.goto(url, wait_until="commit")
          page.locator("#productTitle").wait_for()
          product_title = page.locator("#productTitle").text_content().strip()
          new_price = page.locator(".a-price-symbol").first.text_content().strip() + page.locator(
               ".a-price-whole").first.text_content().strip()
          timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
          int_new_price = int(page.locator(".a-price-whole").first.text_content().strip().replace(",", ""))
          product_rows = df[df[1] == url]


          product_details = [timestamp, url, product_title, int_new_price]
          save_product(product_details)

          print("Product comparison:")
          print("Product title: " + product_title)
          print("Current price: " + new_price)
          if not product_rows.empty:
               latest_price = product_rows.iloc[-1][3]
               if latest_price < int_new_price:
                    print("Previous price: " + page.locator(".a-price-symbol").first.text_content().strip() + str(latest_price))
                    print("Price increased by " + str((int_new_price - latest_price)) + "Rs.")
               elif latest_price > int_new_price:
                    print("Previous price: " + page.locator(
                         ".a-price-symbol").first.text_content().strip() + str(latest_price))
                    print("Price decreased by " + str(abs(int_new_price - latest_price)) + "Rs.")
               else:
                    print("Previous price: " + page.locator(
                         ".a-price-symbol").first.text_content().strip() + str(latest_price))
                    print("No change in product price.")

def scrape_product(page):
     count = 1
     for url in urls:
          page.goto(url, wait_until="commit")
          page.locator("#productTitle").wait_for()
          product_title = page.locator("#productTitle").text_content().strip()
          product_price = page.locator(".a-price-symbol").first.text_content().strip() + page.locator(
               ".a-price-whole").first.text_content().strip()
          int_price = int(page.locator(".a-price-whole").first.text_content().strip().replace(",", ""))
          timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")

          print("\nProduct " + str(count) + ":")
          print("Product title: " + product_title)
          print("Product price: " + product_price)

          product_details = [timestamp, url, product_title, int_price]
          save_product(product_details)
          count += 1

def save_product(data):
     with open(PRICE_FILE, 'a', newline="", encoding="utf8") as csv_file:
          csv_writer = csv.writer(csv_file)
          csv_writer.writerow(data)

def main():
     pw = sync_playwright().start()
     browser = pw.chromium.launch()
     page = browser.new_page()
     get_urls()
     print("Fetching product data...")
     if comp_urls:
          compare_price(page)
     scrape_product(page)
     browser.close()

if __name__ == "__main__":
     main()