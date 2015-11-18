#!/usr/bin/python
import optparse
import sys
import unittest

USAGE = """C:\Program Files (x86)\Google\google_appengine
C:\Users\Kevin\Documents\rateitrepo\code\server\testing
"""


def main(sdk_path, integration_test_path, unit_test_path):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.loader.TestLoader().discover(integration_test_path)
    print("Integration Tests")
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.loader.TestLoader().discover(unit_test_path)
    print("Unit Tests")
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()

    SDK_PATH = "C:\Program Files (x86)\Google\google_appengine"
    INTEGRATION_TEST_PATH = "testing\integration"
    UNIT_TEST_PATH = "testing\unit"
    main(SDK_PATH, INTEGRATION_TEST_PATH, UNIT_TEST_PATH)
