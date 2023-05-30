import subprocess
import pandas as pd
import json

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

