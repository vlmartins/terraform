import subprocess
import json

#subprocess.run(["terraform", "init"])
subprocess.run(["terraform", "apply", "-auto-approve", "-var-file=users.tfvars"])
command = ["terraform", "output", "-json", "instance_details"]

with open('user.json', 'w') as f:
    subprocess.run(command, stdout=f)