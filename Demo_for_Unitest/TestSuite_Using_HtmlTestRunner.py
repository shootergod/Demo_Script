
import os
import unittest
from HTMLTestRunner import HTMLTestRunner

from TestMyCase1 import TestMyCase1
from TestMyCase2 import TestMyCase2

# init a test suite
suite = unittest.TestSuite()


# ============================================================
# option 7
# using html test runner to generate report
# ============================================================

module_path = os.path.dirname(__file__)
reports_dir = os.path.join(module_path, 'reports')
reports_fn = os.path.join(reports_dir, 'html_reports.html')

if not os.path.exists(reports_dir):
    os.mkdir(reports_dir)
if os.path.isfile(reports_fn):
    os.remove(reports_fn)

suite = unittest.defaultTestLoader.discover(
    start_dir=module_path, pattern="TestMyCase*.py")


# ============================================================
# run targets, using html test runner
# ============================================================

with open(reports_fn, 'wb') as rf:
    # runner = unittest.TextTestRunner()
    runner = HTMLTestRunner(title="ABC", description="AAABBBCCC", stream=rf)
    runner.run(suite)
