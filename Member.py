from Cryptography import (decrypt_data, private_key)
# logging
from Log_config import logger

def ShowData(member):
    print(f"> Name:         {decrypt_data(private_key(), member[2])} {decrypt_data(private_key(), member[3])}")
    print(f"> Member ID:    {member[0]}")
    print(f"> User ID:      {member[1]}")
    print(f"> Age:          {decrypt_data(private_key(), member[4])}")
    print(f"> Gender:       {decrypt_data(private_key(), member[5])}")
    print(f"> Weight:       {decrypt_data(private_key(), member[6])}")
    print("> Address")
    print(f"     Street:          {decrypt_data(private_key(), member[7])}")
    print(f"     House Number:    {decrypt_data(private_key(), member[8])}")
    print(f"     Postal Code:     {decrypt_data(private_key(), member[9])}")
    print(f"     City:            {decrypt_data(private_key(), member[10])}")
    print(f"     Country:         {decrypt_data(private_key(), member[11])}")
    print(f"> Email:        {decrypt_data(private_key(), member[12])}")
    print(f"> Phone Number: {decrypt_data(private_key(), member[13])}")
