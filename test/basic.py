#!/usr/bin/env python
"""
mbed SDK
Copyright (c) 2011-2015 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
<<<<<<< HEAD
<<<<<<< HEAD

class BasicTestCase(unittest.TestCase):
    """ Basic true asserts to see that testing is executed
    """
=======
=======
>>>>>>> origin/testing
import os
import errno
import logging


class BasicTestCase(unittest.TestCase):
<<<<<<< HEAD
>>>>>>> ARMmbed/testing
=======
>>>>>>> origin/testing

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_example(self):
        self.assertEqual(True, True)
        self.assertNotEqual(True, False)

if __name__ == '__main__':
    unittest.main()
