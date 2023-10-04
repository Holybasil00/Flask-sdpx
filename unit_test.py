#unit test 01
import unittest
import app

class TestStringMethods(unittest.TestCase):

    def test_test(self):
        self.assertEqual(app.test(), "test")

if __name__ == '__main__':
    unittest.main()