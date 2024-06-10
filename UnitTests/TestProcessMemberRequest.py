import unittest
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Consultant

class TestProcessMemberRequest(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        "John", "Doe",  # First and last name
        "25",           # Age
        "Male",         # Gender
        "70",           # Weight
        "Main Street",  # Street
        "123",          # House number
        "1234 AB",      # Postal code
        "Rotterdam",    # City
        "Netherlands",  # Country
        "john.doe@example.com",  # Email
        "+1234567890"   # Phone number
    ])
    @patch('builtins.print')
    @patch('sqlite3.connect')
    def test_process_member_request(self, mock_connect, mock_print, mock_input):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        
        # Create mock fetchone responses
        def fetchone_side_effect():
            if not hasattr(fetchone_side_effect, "call_count"):
                fetchone_side_effect.call_count = 0
            if fetchone_side_effect.call_count == 0:
                fetchone_side_effect.call_count += 1
                return (1, 'John', 'Doe')  # User exists
            else:
                return None  # User is not already a member
        
        mock_cursor.fetchone.side_effect = fetchone_side_effect
        mock_cursor.execute.return_value = mock_cursor  # Execute should return the mock cursor itself
        
        Consultant.process_member_request()

        # Asserting that appropriate SQL queries were executed
        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_connection.commit.called)
        self.assertTrue(mock_connection.close.called)
        
        # Ensure print was called with success message
        mock_print.assert_called_with("Member request processed successfully")

if __name__ == '__main__':
    unittest.main()
