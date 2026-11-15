import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import app  # noqa: E402


class TestTrucks(unittest.TestCase):
    def test_hay_un_truck_inicial(self):
        self.assertEqual(len(app.TRUCKS), 1)
        self.assertEqual(app.TRUCKS[0]["pueblo"], "Caguas")


if __name__ == "__main__":
    unittest.main()
