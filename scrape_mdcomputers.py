from playwright.sync_api import sync_playwright
import sys

def scrape_products(search_term):
    url = f"https://mdcomputers.in/index.php?route=product/search&search={search_term}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        )

        page.goto(url, wait_until="networkidle")

        products = page.locator(".product-layout")

        if products.count() == 0:
            print("No products found.")
            browser.close()
            return

        for i in range(products.count()):
            product = products.nth(i)

            try:
                name = product.locator(".caption h4").inner_text()
            except:
                name = "N/A"

            try:
                price = product.locator(".price").inner_text()
            except:
                price = "N/A"

            try:
                link = product.locator(".caption h4 a").get_attribute("href")
            except:
                link = "N/A"

            print("=" * 60)
            print("Name :", name)
            print("Price:", price)
            print("Link :", link)

        browser.close()


if __name__ == "__main__":
    term = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "external harddrive"
    scrape_products(term)