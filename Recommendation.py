import os
import google.generativeai as genai
import pandas as pd


# Configure the API key
GOOGLE_API_KEY = ""  
genai.configure(api_key=GOOGLE_API_KEY)

def legacy_user_recommendation(UserID):
   
        # Configure the API key
    GOOGLE_API_KEY = ""  
    genai.configure(api_key=GOOGLE_API_KEY)



    # Initialize Gemini-1.0-Pro model (free version)
    model = genai.GenerativeModel('gemini-1.0-pro')



    user_data = pd.read_csv('userdata.csv')
        
    # Get the index where UserID matches 'bingus'
    index = user_data[user_data['UserID'] == UserID].index[0]

    age = user_data.loc[index, 'Age']
    location = user_data.loc[index, 'Location']
    history = user_data.loc[index, 'PurchaseHistory']

    age, location, history
    # Rest of the code remains the same
    prompt = f"""
    Given a person who is {age} years old and lives in {location}, 
    suggest 4 healthy grocery items they might be interested in buying.
    Also note that they have previously purchased the following items: {history}
    Return only the product names seperated with : do not put indices"""


    response = model.generate_content(prompt)
    recommendation = response.text.strip().split('\n')
    products = [item.strip('- ').strip() for item in recommendation[:5]]

    
    try:
        response = model.generate_content(prompt)
        recommendation = response.text.strip().split('\n')
        products = [item.strip('- ').strip() for item in recommendation[:5]]
        return products
        
    except Exception as e:
        return f"Error occurred: {str(e)}"

def new_user_recommendation(UserID):
    # Initialize Gemini-1.0-Pro model (free version)
    model = genai.GenerativeModel('gemini-1.0-pro')
    # Read the CSV file once
    user_data = pd.read_csv('userdata.csv')
    
    # Read the CSV file once
    user_data = pd.read_csv('userdata.csv')
    
   # Get the index where UserID matches 'bingus'
    index = user_data[user_data['UserID'] == UserID].index[0]

    age = user_data.loc[index, 'Age']
    location = user_data.loc[index, 'Location']
    
    # Rest of the code remains the same
    prompt = f"""
    Given a person who is {age} years old and lives in {location}, 
    suggest 4 healthy grocery items they might be interested in buying. 
    Return only the product names seperated with :. do not put indices"""
    
    try:
        response = model.generate_content(prompt)
        recommendation = response.text.strip().split('\n')
        products = [item.strip('- ').strip() for item in recommendation[:5]]
        return products
        
    except Exception as e:
        return f"Error occurred: {str(e)}"
    



