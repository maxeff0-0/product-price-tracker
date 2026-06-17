from playwright.sync_api import sync_playwright
import csv
from datetime import datetime

urls = []

def get_urls():
     global urls
     url_no = int(input("Enter number of products: "))
     url_count = url_no
     with open('D:/Projects/product-price-tracker/data/products.txt', 'r', encoding="utf-8") as products_file:
          all_urls = products_file.read()
          print("Enter the urls:")
          for i in range(0, url_count):
              url = input()
              url = clean_url(url)
              if url in all_urls:
                  print("Duplicate url entered.\n")
                  continue
              with open('D:/Projects/product-price-tracker/data/products.txt', 'a', encoding="utf-8") as prod_write_file:
                  prod_write_file.write(f"{url}\n")
                  urls.append(url)

def clean_url(url):
     str1 = url.split("dp/")
     str2 = str1[1].split("/")[0] + "/"
     product_url = str1[0] + "dp/" + str2
     return product_url

def scrape_product(page):
     count = 1
     for url in urls:
          page.goto(url)
          page.locator("#productTitle").wait_for()
          product_title = page.locator("#productTitle").text_content().strip()
          product_price = page.locator(".a-price-symbol").first.text_content().strip() + page.locator(
               ".a-price-whole").first.text_content().strip()
          timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")

          print("\nProduct " + str(count) + ":")
          print("Product title: " + product_title)
          print("Product price: " + product_price)

          product_details = [timestamp, product_title, product_price]
          save_product(product_details)
          count += 1

def save_product(data):
     with open('D:/Projects/product-price-tracker/data/prices.csv', 'a', newline="", encoding="utf8") as csv_file:
          csv_writer = csv.writer(csv_file)
          csv_writer.writerow(data)

def main():
     pw = sync_playwright().start()
     browser = pw.chromium.launch()
     page = browser.new_page()
     get_urls()
     print("Fetching product data...")
     scrape_product(page)
     browser.close()

if __name__ == "__main__":
     main()