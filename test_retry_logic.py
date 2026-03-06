import unittest
from unittest.mock import MagicMock, patch
import json
import requests
from utils import fetch_json

class TestFetchJsonRetry(unittest.TestCase):
    @patch('utils.requests.get')
    @patch('utils.time.sleep') # Don't actually sleep
    def test_fetch_json_extra_data_retry(self, mock_sleep, mock_get):
        """Test that fetch_json retries on JSONDecodeError (Extra data)."""
        
        # Mock a response that raises JSONDecodeError
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        # side_effect for json(): fail twice, then succeed
        def side_effect():
            # Simulate "Extra data" error
            raise json.JSONDecodeError("Extra data", "doc", 163935)
            
        mock_response.json.side_effect = [
            json.JSONDecodeError("Extra data", "doc", 163935), # Attempt 1 Fail
            json.JSONDecodeError("Expecting value", "doc", 0), # Attempt 2 Fail
            {"status": "ok"} # Attempt 3 Success
        ]
        
        mock_get.return_value = mock_response
        
        print("\nTesting retry logic for JSON errors...")
        data = fetch_json("http://fake.url")
        
        self.assertIsNotNone(data)
        self.assertEqual(data, {"status": "ok"})
        self.assertEqual(mock_get.call_count, 3)
        print("Successfully retried and recovered from JSON errors.")

if __name__ == '__main__':
    unittest.main()
