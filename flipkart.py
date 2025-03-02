from bs4 import BeautifulSoup
import requests
import re

def flipkart(item):

    def popular(item):
        url = "https://www.flipkart.com/search?q=" + item + "&as-show=on&as=off&sort=popularity"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        product_links = []
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if '/p/' in link:
                full_link = "https://www.flipkart.com" + link if not link.startswith('http') else link
                product_links.append(full_link)
                if len(product_links) == 1:
                    break

        names = []
        prices = []
        links = []
        image_links = []

        for url in product_links:
            product = get_flipkart_details(url)
            names.append(product['name'])
            prices.append(product['price'])
            links.append(url)
            image_links.append(product['image'])
                
        
        return names, prices, links, image_links
    def cheap(item):
        url = "https://www.flipkart.com/search?q=" + item + "&as-show=on&as=off&sort=price_asc"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        product_links = []
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if '/p/' in link:
                full_link = "https://www.flipkart.com" + link if not link.startswith('http') else link
                product_links.append(full_link)
                if len(product_links) == 1:
                    break

        names = []
        prices = []
        links = []
        image_links = []

        for url in product_links:
            product = get_flipkart_details(url)
            names.append(product['name'])
            prices.append(product['price'])
            links.append(url)
            image_links.append(product['image'])
                
        
        return names, prices, links, image_links
    
    def get_flipkart_details(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_name = soup.find('span', {'class': 'VU-ZEz'})
            name = product_name.text.strip() if product_name else "Name not found"
            
            price_element = soup.find('div', {'class': 'Nx9bqj'})
            price = price_element.text.strip() if price_element else "Price not found"
            price = re.sub(r'[^\d.]', '', price)
            
            # Find image link
            image_element = soup.find('img', {'class': 'DByuf4 IZexXJ jLEJ7H'})
            image_link = image_element['src'] if image_element else "Image not found"
            
            return {
            'name': name,
            'price': float(price) if price.replace('.','',1).isdigit() else None,
            'image': image_link
            }
            
        except Exception as e:
            return {
            'name': f"Error: {str(e)}",
            'price': None,
            'image': None
            }

    pop_names, pop_prices, pop_links, pop_image_links = popular(item)
    cheap_names, cheap_prices, cheap_links, cheap_image_links = cheap(item)

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

