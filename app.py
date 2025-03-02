from flask import Flask, request, jsonify
from flask_cors import CORS
from flipkart import flipkart
from bigbasket import bigbasket
from naturesbasket import naturesbasket
from data_functions import register_user, login_user
from Recommendation import legacy_user_Recommendation, new_user_Recommendation
import pandas as pd
from data_functions import end_session

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search_products():
    data = request.get_json()
    search_term = data.get('search_term')
    
    try:
        # Get results from all sources
        flipkart_results = flipkart(search_term)
        bigbasket_results = bigbasket(search_term)
        naturesbasket_results = naturesbasket(search_term)
        
        # Get popular items and filter out invalid ones
        popular_items = []
        
        # Add Flipkart popular item if valid
        if (flipkart_results[0] and flipkart_results[1] and flipkart_results[2] and flipkart_results[3] and 
            flipkart_results[0][0] != "Name not found" and 
            flipkart_results[1][0] is not None):
            popular_items.append({
                'name': flipkart_results[0][0],
                'price': flipkart_results[1][0],
                'link': flipkart_results[2][0],
                'image': flipkart_results[3][0],
                'source': 'Flipkart'
            })
            
        # Add BigBasket popular item if valid
        if (bigbasket_results[0] and bigbasket_results[1] and bigbasket_results[2] and bigbasket_results[3] and 
            bigbasket_results[0][0] != "Name not found" and 
            bigbasket_results[1][0] is not None):
            popular_items.append({
                'name': bigbasket_results[0][0],
                'price': bigbasket_results[1][0],
                'link': bigbasket_results[2][0],
                'image': bigbasket_results[3][0],
                'source': 'BigBasket'
            })
            
        # Add Nature's Basket popular item if valid
        if (naturesbasket_results[0] and naturesbasket_results[1] and naturesbasket_results[2] and naturesbasket_results[3] and 
            naturesbasket_results[0][0] != "Name not found" and 
            naturesbasket_results[1][0] is not None):
            popular_items.append({
                'name': naturesbasket_results[0][0],
                'price': naturesbasket_results[1][0],
                'link': naturesbasket_results[2][0],
                'image': naturesbasket_results[3][0],
                'source': 'Nature\'s Basket'
            })

        # Combine all cheap items into one list and filter out invalid ones
        all_cheap_items = []
        
        # Add Flipkart cheap items
        for name, price, link, image in zip(flipkart_results[4], flipkart_results[5], flipkart_results[6], flipkart_results[7]):
            if price and name != "Name not found" and price > 0:
                all_cheap_items.append({
                    'name': name,
                    'price': price,
                    'link': link,
                    'image': image,
                    'source': 'Flipkart'
                })
        
        # Add BigBasket cheap items
        for name, price, link, image in zip(bigbasket_results[4], bigbasket_results[5], bigbasket_results[6], bigbasket_results[7]):
            if price and name != "Name not found" and price > 0:
                all_cheap_items.append({
                    'name': name,
                    'price': price,
                    'link': link,
                    'image': image,
                    'source': 'BigBasket'
                })
        
        # Add Nature's Basket cheap items
        for name, price, link, image in zip(naturesbasket_results[4], naturesbasket_results[5], naturesbasket_results[6], naturesbasket_results[7]):
            if price and name != "Name not found" and price > 0:
                all_cheap_items.append({
                    'name': name,
                    'price': price,
                    'link': link,
                    'image': image,
                    'source': 'Nature\'s Basket'
                })
        
        # Sort by price and get the cheapest 3 valid items
        cheapest_items = sorted(all_cheap_items, key=lambda x: float(x['price']))[:3]
        
        results = {
            'popular': popular_items,
            'cheapest': cheapest_items
        }
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    userid = data.get('userid')
    password = data.get('password')
    age = data.get('age')
    location = data.get('location')
    
    try:
        result = register_user(userid, password, age, location)
        if isinstance(result, tuple):
            success, message = result
            return jsonify({'success': success, 'message': message})
        return jsonify({'success': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    userid = data.get('userid')
    password = data.get('password')
    
    try:
        result = login_user(userid, password)
        if isinstance(result, tuple):
            success, message = result
            return jsonify({'success': success, 'message': message})
        return jsonify({'success': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/Recommendation', methods=['POST'])
def get_Recommendation():
    data = request.get_json()
    userid = data.get('userid')
    
    try:
        df = pd.read_csv('userdata.csv')
        user_data = df[df['UserID'] == userid]
        
        print(f"\n=== Getting Recommendation for user: {userid} ===")
        
        # Get Recommendation
        if not user_data.empty and 'PurchaseHistory' in user_data.columns and pd.notna(user_data['PurchaseHistory'].iloc[0]):
            print("Using legacy Recommendation")
            raw_Recommendation = legacy_user_Recommendation(userid)
        else:
            print("Using new user Recommendation")
            raw_Recommendation = new_user_Recommendation(userid)
            
        print(f"\nRaw Recommendation: {raw_Recommendation}")
        
        # Extract items from first element if it's a list with one string containing colons
        if isinstance(raw_Recommendation, list) and len(raw_Recommendation) == 1 and ':' in raw_Recommendation[0]:
            items = [item.strip() for item in raw_Recommendation[0].split(':')]
        elif isinstance(raw_Recommendation, list):
            items = raw_Recommendation
        else:
            items = [raw_Recommendation]  # Handle single string case
            
        print(f"\nProcessing these items: {items}")
        
        # Process each item through search
        recommended_products = []
        for item in items:
            if not item:  # Skip empty items
                continue
                
            try:
                print(f"\nProcessing recommendation: {item}")
                search_results = {
                    'flipkart': flipkart(item),
                    'bigbasket': bigbasket(item),
                    'naturesbasket': naturesbasket(item)
                }
                
                # Get valid products from each source
                all_items = []
                
                for source, results in search_results.items():
                    if results[0] and results[1] and len(results[0]) > 0:
                        all_items.append({
                            'name': results[0][0],
                            'price': results[1][0],
                            'link': results[2][0],
                            'image': results[3][0],
                            'source': source.title()
                        })
                
                # Add cheapest product for this item
                if all_items:
                    cheapest = min(all_items, key=lambda x: float(x['price']))
                    recommended_products.append(cheapest)
                    print(f"Added product for {item}: {cheapest['name']} from {cheapest['source']}")
            
            except Exception as e:
                print(f"Error processing {item}: {str(e)}")
                continue
        
        print(f"\nFinal Recommendation count: {len(recommended_products)}")
        print("Recommendation:", recommended_products)
        
        return jsonify({
            'success': True, 
            'Recommendation': recommended_products,
            'count': len(recommended_products)
        })
        
    except Exception as e:
        print(f"Recommendation error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/end_session', methods=['POST'])
def handle_end_session():
    data = request.get_json()
    userid = data.get('userid')
    cart_items = data.get('cart_items')
    
    try:
        success = end_session(userid, cart_items)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
        
if __name__ == '__main__':
    app.run(debug=True)