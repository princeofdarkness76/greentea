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

import json
from meshtest_base import MbedGreenteaMeshRunnerInterface


class BLEMeshRunner(MbedGreenteaMeshRunnerInterface):
    def __init__(self, options=None):
        MbedGreenteaMeshRunnerInterface.__init__(options=options)
        self.config = None

    def setup(self):
        self.config = self.read_config()

    def run(self):
        pass

    def print_config(self):
        pass

    def read_config(self, config_name=None):
        result = None
        if not config_name:
            config_name = self.DEFAULT_CONFIG
        try:
            with open(config_name) as f:
                result = json.load(f)
        except Exception as e:
            gt_log_err(str(e))
        return result


def main_meshtest_cli(opts, args, gt_instance_uuid=None):
    """
    * read config.json
    * mbedls
    * select avail modes
      * build nodes using yotta with avail targets or
      * use absolute path or
      * use external command <future>
    * flash nodes
    * reset
    * assign node number
    * sync and capture golden log

    """
    print "mesh testing!"
