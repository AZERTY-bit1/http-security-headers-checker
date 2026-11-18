import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from headers_checker import grade  # noqa: E402


class TestHeaders(unittest.TestCase):
    def test_no_headers(self):
        self.assertEqual(grade({})["grade"], "F")

    def test_all_headers(self):
        h = {k: "x" for k in ["Strict-Transport-Security", "Content-Security-Policy",
                              "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy",
                              "Permissions-Policy", "Cross-Origin-Opener-Policy"]}
        self.assertEqual(grade(h)["grade"], "A")

    def test_leak(self):
        self.assertIn("Server: Apache/2.4.1", grade({"Server": "Apache/2.4.1"})["leaks"])


if __name__ == "__main__":
    unittest.main()
