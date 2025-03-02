import pandas as pd
import os

def register_user(userid, password, age, location):
    # Define the CSV file path
    csv_file = 'userdata.csv'
    
    # Check if file exists, if not create with headers
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=['UserID', 'Password', 'Age', 'Location'])
        df.to_csv(csv_file, index=False)
    
    # Read existing data
    df = pd.read_csv(csv_file)
    
    # Check if UserID already exists
    if userid in df['UserID'].values:
        return False, "UserID already exists"
    
    # Create new row of data
    new_user = pd.DataFrame({
        'UserID': [userid],
        'Password': [password],
        'Age': [age],
        'Location': [location]
    })
    
    # Append new user data to CSV
    new_user.to_csv(csv_file, mode='a', header=False, index=False)
    
    return True

def login_user(userid, password):
    # Check if file exists
    if not os.path.exists('userdata.csv'):
        return False, "No users registered"

    # Read the CSV file
    df = pd.read_csv('userdata.csv')

    # Check if userid exists and password matches
    mask = (df['UserID'] == userid) & (df['Password'] == password)
    if mask.any():
        return True
    else:
        return False

def end_session(UserID, cartItems):
        # Read the user data
        df = pd.read_csv('userdata.csv')

        # If 'PurchaseHistory' column doesn't exist, create it
        if 'PurchaseHistory' not in df.columns:
            df['PurchaseHistory'] = ''

        # Update purchase history for the user
        mask = df['UserID'] == UserID
        if mask.any():
            # Convert cart items to string and append to existing history
            existing_history = str(df.loc[mask, 'PurchaseHistory'].iloc[0])
            new_history = existing_history + str(cartItems) if existing_history else str(cartItems)
            df.loc[mask, 'PurchaseHistory'] = new_history
            
            # Save updated dataframe
            df.to_csv('userdata.csv', index=False)
            return True
        return False

