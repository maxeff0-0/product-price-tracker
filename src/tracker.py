from playwright.sync_api import sync_playwright

pw = sync_playwright().start()

browser = pw.chromium.launch(
    headless=False,
    slow_mo=2000
)
page = browser.new_page()
user_url = input("Enter product url(amazon): ")
str1 = user_url.split("dp/")
str2 = str1[1].split("/")[0] + "/"
product_url = str1[0] + "dp/" + str2
page.goto(product_url)
print("\nFetching product details...")

product_title = page.locator("#productTitle").text_content().strip()
product_price = page.locator(".a-price-symbol").first.text_content().strip() + page.locator(".a-price-whole").first.text_content().strip()

print("\nProduct title: " + product_title)
print("Product price: " + product_price)

browser.close()