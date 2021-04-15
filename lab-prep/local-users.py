#!/usr/bin/python3
'''
Read user list from csv and create users in format name.lastname
'''

import sys, uuid
from subprocess import Popen, PIPE
import pandas as pd

# Input data
userfile = "Lista MTI-2020.csv"
# Skiprows if static data is present
df = pd.read_csv(userfile, skiprows=[0,1,2])
name_col = "E-MAIL INSTITUCIONAL"

# Output data
user_dict = {}
# If a param is passed
if len(sys.argv) > 1:
    try:
        only_pass = bool(sys.argv[1])
        print(only_pass)
    except Exception as e:
        print(f"Cant interpret param as True or False: {e}")

for row in df[name_col]:
    # Use email name without domain
    try:
        name = row.split("@")[0]
    except Exception as e:
        print(f"Cant select name from {row}: {e}")
        continue

    # Call useradd
    if only_pass == False:
        create_user = Popen([f"useradd -U {name}"], stdout=PIPE,stderr=PIPE, shell=True)
        out, err = create_user.communicate()
        # Return code 0 is success, else ...
        if create_user.returncode:
            print(f"Cant create user {name}. Out: {out}, err:{err}")
            continue

    # Assign a random password, with only 10 digits
    pword = uuid.uuid4().hex[:10]
    mod_pass = Popen([f"echo {pword} | echo {pword} | passwd {name}"], stdout=PIPE,stderr=PIPE, shell=True)
    out, err = mod_pass.communicate()
    # Return code 0 is success, else ...
    if mod_pass.returncode:
        print(f"Cant assign password to user {name}. Out: {out}, err:{err}")

    # Store data in user dict
    user_dict[name] = pword
    print(f"New user {name} OK")
# Finally, save user dict as csv through pandas
print(user_dict)
df_out = pd.DataFrame.from_dict(user_dict)
df_out.to_csv("alumnos2020.csv")
