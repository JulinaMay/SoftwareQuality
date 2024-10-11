from safe_data import (decrypt_data, private_key)
# logging.
from log_config import logmanager as log_manager
log_instance = log_manager()

def ShowData(member):
    print(f"> Name:         {member[1]} {member[2]}")
    print(f"> Member ID:    {member[0]}")
    print(f"> Age:          {member[3]}")
    print(f"> Gender:       {member[4]}")
    print(f"> Weight:       {member[5]}")
    print("> Address")
    print(f"     Street:          {member[6]}")
    print(f"     House Number:    {member[7]}")
    print(f"     Postal Code:     {member[8]}")
    print(f"     City:            {member[9]}")
    print(f"     Country:         {member[10]}")
    print(f"> Email:        {member[11]}")
    print(f"> Phone Number: {member[12]}")
