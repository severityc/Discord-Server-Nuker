import requests

def get_bot_id(token):
    headers = {
        'Authorization': f'Bot {token}',
    }
    
    response = requests.get('https://discord.com/api/users/@me', headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        return user_data['id']
    else:
        return None

# Prompt the user to enter the bot token
bot_token = input("Enter your bot token: ")

bot_id = get_bot_id(bot_token)

if bot_id:
    print(f"Bot ID: {bot_id}")
else:
    print("Failed to get bot ID. Check your bot token.")
