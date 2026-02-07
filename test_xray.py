import unittest
from utils import check_xray_flux, get_xray_data

class TestXRay(unittest.TestCase):
    def test_fetch_xray(self):
        """Test fetching X-ray data from NOAA."""
        print("Fetching X-ray data...")
        data = get_xray_data()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        print("Successfully fetched X-ray data.")
        
        # Print a sample
        print("Sample data entry:", data[0])
        self.assertIn('flux', data[0])
        self.assertIn('energy', data[0])

    def test_check_xray_flux_no_alert(self):
        """Test logic with low flux."""
        mock_data = [
            {"time_tag": "2024-01-01T00:00:00Z", "flux": 1e-6, "energy": "0.1-0.8nm"},
            {"time_tag": "2024-01-01T00:01:00Z", "flux": 2e-6, "energy": "0.1-0.8nm"}
        ]
        result = check_xray_flux(mock_data)
        self.assertIsNone(result)

    def test_check_xray_flux_alert_r1(self):
        """Test logic with R1 flux."""
        mock_data = [
            {"time_tag": "2024-01-01T00:00:00Z", "flux": 1e-6, "energy": "0.1-0.8nm"},
            {"time_tag": "2024-01-01T00:01:00Z", "flux": 1.5e-5, "energy": "0.1-0.8nm"} # > 1e-5
        ]
        result = check_xray_flux(mock_data)
        self.assertIsNotNone(result)
        self.assertEqual(result['scale'], "R1 (Minor)")
        self.assertEqual(result['flux'], 1.5e-5)

    def test_check_xray_flux_alert_r3(self):
        """Test logic with R3 flux."""
        mock_data = [
            {"time_tag": "2024-01-01T00:00:00Z", "flux": 1e-6, "energy": "0.1-0.8nm"},
            {"time_tag": "2024-01-01T00:01:00Z", "flux": 2e-4, "energy": "0.1-0.8nm"} # > 1e-4
        ]
        result = check_xray_flux(mock_data)
        self.assertIsNotNone(result)
        self.assertEqual(result['scale'], "R3 (Strong)")

    def test_check_xray_flux_wrong_energy(self):
        """Test ignoring wrong energy channel."""
        mock_data = [
            {"time_tag": "2024-01-01T00:00:00Z", "flux": 1.0, "energy": "0.05-0.4nm"} # High flux but wrong channel
        ]
        result = check_xray_flux(mock_data)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
