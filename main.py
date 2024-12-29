import os, sys, time, random, string
try:
    import requests
except:
    os.system('pip install requests')
import requests

# Line Function
def linex():
    print("================================================")

# Clear terminal session
def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

# Get Captcha token
def get_token():
    while True:
        res = requests.get(f'http://localhost:5000/get').text
        if 'None' not in res:
            print(">> Captcha token retrieved successfully")
            return res
        else:
            time.sleep(0.5)

# Get headers set / with `auth_token` or head only
def get_headers(auth_token=None):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://app.nodepay.ai',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
        headers['origin'] = 'chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm'
    return headers

# Login account
def login_accounts(email, password, captcha_token):
    try:
        json_data = {
            'user': email,
            'password': password,
            'remember_me': True,
            'recaptcha_token': captcha_token
        }
        headers = get_headers()
        url = "https://api.nodepay.ai/api/auth/login"
        response = requests.post(url, headers=headers, json=json_data, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {str(e)}")
        linex()
        time.sleep(1)

# Read accounts from file
def read_accounts(filename="accounts.txt"):
    accounts = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                account_info = line.strip().split(',')
                if len(account_info) == 2:
                    accounts.append((account_info[0], account_info[1]))
    except Exception as e:
        print(f"Failed to read accounts from file: {e}")
    return accounts

# Save JWT token to file
def save_token(token, filename="token_list.txt"):
    try:
        with open(filename, 'a') as file:
            file.write(f"{token}\n")
    except Exception as e:
        print(f"Failed to save token to file: {e}")

# Main function
def main():
    clear_screen()

    # Read accounts from file
    accounts = read_accounts()

    if not accounts:
        print("No accounts found in the file. Exiting...")
        exit()

    # Process each account
    for email, password in accounts:
        print(f"Logging in with {email}...")
        captcha_token = get_token()

        login_response = login_accounts(email, password, captcha_token)

        if login_response.get('msg') == 'Success':
            print(f"Account Login Successfully: {email}")
            auth_token = login_response['data']['token']
            print(f"JWT Token: {auth_token}")

            # Save token to file
            save_token(auth_token)
        else:
            print(f"Login Failed: {login_response.get('msg')}")

        linex()

    print("All accounts processed.")
    exit()

main()
