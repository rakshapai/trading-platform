import os
import pyotp
from robin_stocks import *
import robin_stocks.robinhood as r
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure environment variables are loaded correctly
username = os.getenv('robin_username')
password = os.getenv('robin_password')
mfa_secret = os.getenv('robin_mfa')

if not username or not password or not mfa_secret:
    raise ValueError("Error: Missing environment variables. Check your .env file.")

# # Generate TOTP for two-factor authentication
# totp = pyotp.TOTP(mfa_secret).now()
# print("Current OTP:", totp)

def login():
    """Login to Robinhood account. Each login expires in 1 hour"""
    r.login(username, password, expiresIn=3600)
        

# Function to get the latest stock price
def QUOTE(ticker):
    try:
        price = r.stocks.get_latest_price(ticker)
        if price:
            print(f"{ticker.upper()}: ${price[0]}")
        else:
            print(f"Error: Could not fetch price for {ticker}")
    except Exception as e:
        print(f"Error retrieving price for {ticker}: {str(e)}")
