import json
from gmail import send_email

# Load the JSON data
with open("user.json") as f:
    data = json.load(f)

# Split the keys into username and email, and map them to their IP addresses
users = [
    {
        "name": key.split(":")[0],
        "email": key.split(":")[1],
        "ip_address": value
    }
    for key, value in data.items()
]

# Send the parsed data
#"User: {user['name']}, Email: {user['email']}, IP Address: {user['ip_address']
for user in users:
    message = f"Olá {user['name']}, sua máquina já pode ser acessada no IP público: {user['ip_address']}"
    send_email(user['email'], message)