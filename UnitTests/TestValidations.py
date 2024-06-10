import unittest
from unittest.mock import patch

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Consultant import (
    validate_first_name, validate_last_name, validate_age, validate_gender, 
    validate_weight, validate_street, validate_house_number, validate_postal_code, 
    validate_city, validate_country, validate_email, validate_phone_number
)

class TestValidations(unittest.TestCase):

    def test_validate_first_name(self):
        self.assertFalse(validate_first_name("John"))
        self.assertTrue(validate_first_name("John123"))
        self.assertTrue(validate_first_name("John!"))
        self.assertTrue(validate_first_name(""))

    def test_validate_last_name(self):
        self.assertFalse(validate_last_name("Doe"))
        self.assertFalse(validate_last_name("O'Connor"))
        self.assertTrue(validate_last_name("Doe123"))
        self.assertTrue(validate_last_name("Doe!"))
        self.assertTrue(validate_last_name(""))

    def test_validate_age(self):
        self.assertFalse(validate_age("25"))
        self.assertTrue(validate_age("-5"))
        self.assertTrue(validate_age("abc"))
        self.assertTrue(validate_age("150"))

    def test_validate_gender(self):
        self.assertFalse(validate_gender("Male"))
        self.assertTrue(validate_gender("Unknown"))

    def test_validate_weight(self):
        self.assertFalse(validate_weight("70"))
        self.assertTrue(validate_weight("-5"))
        self.assertTrue(validate_weight("abc"))
        self.assertTrue(validate_weight("500"))

    def test_validate_street(self):
        self.assertFalse(validate_street("Main Street"))
        self.assertTrue(validate_street("Main Street!"))
        self.assertTrue(validate_street(""))

    def test_validate_house_number(self):
        self.assertFalse(validate_house_number("123"))
        self.assertTrue(validate_house_number("-1"))
        self.assertTrue(validate_house_number("abc"))

    def test_validate_postal_code(self):
        self.assertFalse(validate_postal_code("1234 AB"))
        self.assertTrue(validate_postal_code("12345 ABC"))

    def test_validate_city(self):
        self.assertFalse(validate_city("Rotterdam"))
        self.assertTrue(validate_city("Amsterdam"))
        self.assertTrue(validate_city("Unknown City"))

    def test_validate_country(self):
        self.assertFalse(validate_country("Netherlands"))
        self.assertTrue(validate_country("Netherlands123"))
        self.assertTrue(validate_country("netherlands"))

    def test_validate_email(self):
        self.assertFalse(validate_email("test@example.com"))
        self.assertTrue(validate_email("test@example"))
        self.assertTrue(validate_email("test@.com"))

    def test_validate_phone_number(self):
        self.assertFalse(validate_phone_number("+1234567890"))
        self.assertTrue(validate_phone_number("1234567890"))
        self.assertTrue(validate_phone_number("+12 34 56"))
        self.assertTrue(validate_phone_number(""))

if __name__ == '__main__':
    unittest.main()
