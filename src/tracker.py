from playwright.sync_api import sync_playwright

pw = sync_playwright().start()

browser = pw.chromium.launch(
    headless=False,
    slow_mo=2000
)
page = browser.new_page()
user_url = input("Enter product url(amazon): ")
str1 = user_url.split("dp/")
str2 = str1[1]
product_url = str1[0] + "dp/" + str2.split("/")[0] + "/"
page.goto(product_url)
browser.close()