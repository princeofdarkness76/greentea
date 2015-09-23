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

import json
import unittest

from mbed_greentea.mbedgt_meshtest import meshtest_nodes


class NodeSelectorAlgorithm(unittest.TestCase):
    def setUp(self):
    
        self.AVAIL_PLATFORMS = {
            'A' : 1,
            'B' : 1,
            'C' : 1
        }
        
        self.NODES_DEF = {
            '*' : [],
            '0' : ['A', 'B'],
            '1' : ['A', 'B', 'C'],
            '2' : ['B'],
            }
        pass

    def tearDown(self):
        pass

    def test_xxx(self):
        print
        nodes = meshtest_nodes.gt_select_nodes(self.AVAIL_PLATFORMS, self.NODES_DEF)
        print nodes
    
    def test_permutation(self):
        import itertools
        l = [['A', 'B', 'C'], ['A', 'B'], ['B']]
        print l
        print list(itertools.product(*l))
    
if __name__ == '__main__':
    unittest.main()
