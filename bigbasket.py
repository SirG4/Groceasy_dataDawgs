from bs4 import BeautifulSoup
import requests
import re

def bigbasket(item):

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.bigbasket.com/',
            'Connection': 'keep-alive'
        }

    def popular(item):
        url = "https://www.bigbasket.com/ps/?q=" + item + "&nc=as"
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        product_links = []
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if '/pd/' in link:
                full_link = "https://www.bigbasket.com" + link if not link.startswith('http') else link
                product_links.append(full_link)
                if len(product_links) == 1:
                    break

        names = []
        prices = []
        links = []
        image_links = []
        
        for url in product_links:
            product = get_bigbasket_details(url, headers = headers)
            names.append(product['name'])
            prices.append(product['price'])
            links.append(url)
            image_links.append(product['image'])
        
        return names, prices, links, image_links

    def cheap(item):
        url = "https://www.bigbasket.com/ps/?q=" + item + "&nc=as"
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        product_links = []
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if '/pd/' in link:
                full_link = "https://www.bigbasket.com" + link if not link.startswith('http') else link
                product_links.append(full_link)
                if len(product_links) == 2:
                    break

        names = []
        prices = []
        links = []
        image_links = []
        
        for url in product_links:
            product = get_bigbasket_details(url, headers = headers)
            names.append(product['name'])
            prices.append(product['price'])
            links.append(url)
            image_links.append(product['image'])
        
        return names, prices, links, image_links


    def get_bigbasket_details(url, headers = headers):
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
            
            product_name = soup.find('h1', {'class': 'Description___StyledH-sc-82a36a-2 bofYPK'})
            name = product_name.text.strip() if product_name else "Name not found"
            
            price_element = soup.find('td', {'class': 'Description___StyledTd-sc-82a36a-4 fLZywG'})
            price = price_element.text.strip() if price_element else "Price not found"
            price = re.sub(r'[^\d.]', '', price)
            
            # Find image link - looking for URLs containing the specific pattern
            image_link = None
            for img in soup.find_all('img'):
                if img.get('src') and 'www.bigbasket.com/media/uploads/p/' in img.get('src'):
                    image_link = img.get('src')
                    break
            
            return {
                'name': name,
                'price': float(price) if price.replace('.','',1).isdigit() else None,
                'image': image_link if image_link else "Image not found"
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




