from playwright.sync_api import sync_playwright
import csv
from datetime import datetime

pw = sync_playwright().start()

browser = pw.chromium.launch()
page = browser.new_page()
user_url = input("Enter product url(amazon): ")
str1 = user_url.split("dp/")
str2 = str1[1].split("/")[0] + "/"
product_url = str1[0] + "dp/" + str2
print("\nFetching product details...")
page.goto(product_url)

product_title = page.locator("#productTitle").text_content().strip()
product_price = page.locator(".a-price-symbol").first.text_content().strip() + page.locator(".a-price-whole").first.text_content().strip()
timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")

print("\nProduct title: " + product_title)
print("Product price: " + product_price)

product_details = [timestamp, product_title, product_price]

with open('data/prices.csv', 'a', newline="", encoding="utf8") as csv_file:
     csv_writer = csv.writer(csv_file)
     csv_writer.writerow(product_details)

browser.close()