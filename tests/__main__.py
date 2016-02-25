# -*- coding: utf-8 -*-

import sys
import pytest


if __name__ == '__main__':
    # Exit with correct code
    sys.exit(pytest.main(["--pyargs", "changelog.tests"] + sys.argv[1:]))
