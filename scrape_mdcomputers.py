import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys

def scrape_mdcomputers(search_term):
    encoded_term = urllib.parse.quote(search_term)
    url = f"https://mdcomputers.in/?route=product/search&search={encoded_term}"
    
    # Using headers to mimic a real browser to bypass basic bot protections
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    print(f"Scraping MDComputers for: '{search_term}'\nURL: {url}\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Handle Cloudflare/WAF 403 blocks gracefully
        if response.status_code == 403:
            print("Error: Received 403 Forbidden. MDComputers' firewall is blocking the request.")
            print("Note: Bypassing this would require advanced tools like cloudscraper or Playwright.")
            return
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select(".product-layout")

        if not products:
            print("No products found.")
            return

        for idx, product in enumerate(products, 1):
            try:
                name_elem = product.select_one(".caption h4 a")
                name = name_elem.text.strip() if name_elem else "N/A"
            except Exception:
                name = "N/A"

            try:
                price_elem = product.select_one(".price")
                price = price_elem.text.strip() if price_elem else "N/A"
            except Exception:
                price = "N/A"

            try:
                link_elem = product.select_one(".caption h4 a")
                link = link_elem["href"] if link_elem and "href" in link_elem.attrs else "N/A"
            except Exception:
                link = "N/A"

            print("=" * 60)
            print(f"Product {idx}:")
            print("Name :", name)
            print("Price:", price)
            print("Link :", link)

    except requests.RequestException as e:
        print(f"Request error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    term = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "external harddrive"
    scrape_mdcomputers(term)