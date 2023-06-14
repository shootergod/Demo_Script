import unittest

class TestMyCase2(unittest.TestCase):
    def setUp(self):
        print("-----> setup")

    def tearDown(self):
        print("—-—-—> teardown")

    def test_1(self):
        print("T2 testl")
        self.assertEqual(1,2)

    def test_2(self):
        print("T2 test2")

    def test_3(self):
        print("T2 test3")

    def test_4(self):
        print("T2 test4")

if __name__ == '__main__':
    unittest.main()