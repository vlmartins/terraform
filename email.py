import json

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

# Print the parsed data
for user in users:
    print(f"User: {user['name']}, Email: {user['email']}, IP Address: {user['ip_address']}")