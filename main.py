import subprocess
import pandas as pd
import json
from gmail import send_email

#create list of dictionaries
users = []

#fake user data for testing
# users.append({"user": row['user'], "email": row['email'], "auth_key": row['auth_key']})
# users.append({"user": "jdoe", "email": "jdoe@jdoe.com", "auth_key": "1234"})
# users.append({"user": "alice", "email": "alice@a.com", "auth_key": "2344"})
# users.append({"user": "john", "email": "john@a.com", "auth_key": "2344"})

#users from google sheet
source = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTrO5nSVgoSjm-yJzBiSBfK1KcfULIZ-Mpn2oFjKbRYcixcJ4i4a9aOoggZFB-QW_eaex7gOXTfhhVs/pub?output=csv'

#read csv
df = pd.read_csv(source)

# Iterate over rows to create list of strings containing user data for terraform
for index, row in df.iterrows():
    auth_key = row['pubkey'].rstrip(",\n").rstrip()  # Remove any trailing commas, newlines, and spaces
    user_str = f'  {{\n    name = "{row["hostname"]}",\n    email = "{row["Endereço de e-mail"]}",\n    auth_key = "{auth_key}"\n  }}'
    users.append(user_str)

# Write to file for terraform
with open("users.tfvars", "w") as file:
    file.write('users = [\n')
    file.write(',\n'.join(users))
    file.write('\n]\n')

#run terraform
subprocess.run(["terraform", "init"])
subprocess.run(["terraform", "apply", "-auto-approve", "-var-file=users.tfvars"])
command = ["terraform", "output", "-json", "instance_details"]

with open('user.json', 'w') as f:
    subprocess.run(command, stdout=f)

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