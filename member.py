from safe_data import (decrypt_data, private_key)
# logging.
from log_config import logger

def ShowData(member):
    print(f"> Name:         {member[2]} {member[3]}")
    print(f"> Member ID:    {member[1]}")
    print(f"> Age:          {member[4]}")
    print(f"> Gender:       {member[5]}")
    print(f"> Weight:       {member[6]}")
    print("> Address")
    print(f"     Street:          {member[7]}")
    print(f"     House Number:    {member[8]}")
    print(f"     Postal Code:     {member[9]}")
    print(f"     City:            {member[10]}")
    print(f"     Country:         {member[11]}")
    print(f"> Email:        {member[12]}")
    print(f"> Phone Number: {member[13]}")
