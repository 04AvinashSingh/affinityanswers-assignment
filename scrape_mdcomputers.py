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
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # The standard product container class in MDComputers (OpenCart)
    products = soup.find_all('div', class_='product-layout')
    
    if not products:
        print("No products found or the HTML structure has changed.")
        return

    print(f"Found {len(products)} products on the first page.\n")
    print("-" * 80)
    
    for idx, product in enumerate(products, 1):
        name_elem = product.find('div', class_='name')
        if name_elem and name_elem.find('a'):
            a_tag = name_elem.find('a')
            name = a_tag.text.strip()
            link = a_tag.get('href', '')
        else:
            name, link = "Unknown Name", ""
        
        # Extract product price (handling discounts vs regular prices)
        price_elem = product.find('span', class_='price-new')
        if not price_elem:
            price_elem = product.find('div', class_='price')
            if price_elem:
                # Remove tax text if present inside the price div
                for span in price_elem.find_all('span', class_='price-tax'):
                    span.decompose()
        
        price = price_elem.text.strip() if price_elem else "Price not available"
        
        print(f"{idx}. {name}")
        print(f"   Price: {price}")
        print(f"   Link: {link}")
        print("-" * 80)

if __name__ == "__main__":
    term = "external harddrive"
    if len(sys.argv) > 1:
        term = " ".join(sys.argv[1:])
    scrape_mdcomputers(term)
