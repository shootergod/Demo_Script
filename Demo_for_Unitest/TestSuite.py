
import os
import unittest


from TestMyCase1 import TestMyCase1
from TestMyCase2 import TestMyCase2

# init a test suite
suite = unittest.TestSuite()

# ============================================================
# option 1
# chose the test_func those you want to
# ============================================================
# suite.addTest(TestMyCase1("test_1"))
# suite.addTest(TestMyCase1("test_2"))
# suite.addTest(TestMyCase2("test_3"))
# suite.addTest(TestMyCase2("test_4"))

# ============================================================
# option 2
# using addTests() by pass a list of test_func
# ============================================================
# cases = [TestMyCase1("test_1"), TestMyCase1("test_2"),
#                TestMyCase2("test_3"), TestMyCase2("test_4")]
# suite.addTests(cases)


# ============================================================
# option 3
# add all tests in a module
# ============================================================
# suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMyCase1))


# ============================================================
# option 4
# add tests by name [class]
# ============================================================
# suite.addTests(unittest.TestLoader().loadTestsFromName("TestMyCase1.TestMyCase1"))

# suite.addTests(unittest.TestLoader().loadTestsFromNames(
#     ["TestMyCase1.TestMyCase1", "TestMyCase2.TestMyCase2"]))


# ============================================================
# option 5
# add tests by module
# ============================================================
# suite.addTests(unittest.TestLoader().loadTestsFromModule(TestMyCase1))


# ============================================================
# option 6
# add tests by many file
# ============================================================

module_path = os.path.dirname(__file__)

suite = unittest.defaultTestLoader.discover(
    start_dir=module_path, pattern="TestMyCase*.py")


# ============================================================
# run targets
# ============================================================
runner = unittest.TextTestRunner()
runner.run(suite)
