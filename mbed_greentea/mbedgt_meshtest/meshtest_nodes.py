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

Author: Przemyslaw Wirkus <Przemyslaw.Wirkus@arm.com>
"""

def gt_select_nodes(avail_platforms, nodes_def):
    """! Assigns available platforms to selected nodes
    @return Dictionary { int:node_no : platform_name }
    """
    result = {}

    # All nodes mentioned in nodes description
    all_node_types = []
    for node in nodes_def:
        all_node_types.extend(nodes_def[node])
    all_node_types = set(all_node_types)

    # Remove nodes not available

    print all_node_types

    return result
