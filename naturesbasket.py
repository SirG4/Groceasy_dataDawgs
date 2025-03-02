
from bs4 import BeautifulSoup
import requests
import re
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    }

def naturesbasket(item):\

    def popular(item):
            url = "https://www.naturesbasket.co.in/Online-grocery-shopping/" + item + "?clk"
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')

            product_links = []
            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                if re.search("https://www.naturesbasket.co.in/Products/",link):
                    full_link = "https://www.naturesbasket.co.in/Products/" + link if not link.startswith('http') else link
                    product_links.append(full_link)
                    if len(product_links) == 3:
                        break


            names = []
            prices = []
            links = []
            image_links = []
            
            for url in product_links:
                product = get_naturesbasket_details(url, headers = headers)
                names.append(product['name'])
                prices.append(product['price'])
                links.append(url)
                image_links.append(product['image_link'])
            
        
            return names, prices, links, image_links


    def get_naturesbasket_details(url, headers = headers):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                product_name = soup.find('h1', {'class': 'pd_Title'})
                name = product_name.text.strip() if product_name else "Name not found"
                
                price_element = soup.find('span', {'class': 'search_PSellingP'})  
                price = price_element.text.strip() if price_element else "Price not found"
                price = re.sub(r'[^\d.]', '', price)

                image_links = []
                for img_tag in soup.find_all('img'):
                    src = img_tag.get('src', '')
                    if 'cloudfront.net/ProductVariantThumbnailImages/' in src:
                        image_links.append(src)
                    if len(image_links) == 1:
                        break  
                image_link = image_links[0] if image_links else "Image not found"    
                
                return {
                    'name': name,
                    'price': float(price) if price.replace('.','',1).isdigit() else None,
                    'image_link': image_link
                }
                
            except Exception as e:
                return {
                    'name': f"Error: {str(e)}",
                    'price': None,
                    'image_link': image_link
                }
            
    pop_names, pop_prices, pop_links, pop_image_links = popular(item)

    # Create list of tuples with all product info
    product_info = list(zip(pop_names, pop_prices, pop_links, pop_image_links))

    # Sort by price (handling potential None values)
    sorted_products = sorted(product_info, 
                        key=lambda x: float(x[1]) if x[1] else 0, 
                        reverse=True)

    # Split into expensive and cheap products
    expensive_products = sorted_products[:1]
    cheap_products = sorted_products[-2:]

    # Initialize lists for return values
    pop_names = []
    pop_prices = []
    pop_links = []
    pop_image_links = []
    cheap_names = []
    cheap_prices = []
    cheap_links = []
    cheap_image_links = []

    # Extract popular products
    for name, price, link, image_link in expensive_products:
        pop_names.append(name)
        pop_prices.append(price)
        pop_links.append(link)
        pop_image_links.append(image_link)

    # Extract cheap products
    for name, price, link, image_link in cheap_products:
        cheap_names.append(name)
        cheap_prices.append(price)
        cheap_links.append(link)
        cheap_image_links.append(image_link)

    return (
        pop_names, 
        pop_prices, 
        pop_links, 
        pop_image_links,
        cheap_names, 
        cheap_prices, 
        cheap_links,
        cheap_image_links
    )        






