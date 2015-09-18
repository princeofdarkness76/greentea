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

import os
import sys
import json
from meshtest_base import MbedGreenteaMeshRunnerInterface
from mbed_greentea.mbed_test_api import run_cli_command
from mbed_greentea.mbed_greentea_log import gt_log
from mbed_greentea.mbed_greentea_log import gt_bright
from mbed_greentea.mbed_greentea_log import gt_log_tab
from mbed_greentea.mbed_greentea_log import gt_log_err
from mbed_greentea.mbed_greentea_log import gt_log_warn


try:
    import mbed_lstools
    import mbed_host_tests
except ImportError as e:
    print str(e)

MBED_LMTOOLS = 'mbed_lstools' in sys.modules
MBED_HOST_TESTS = 'mbed_host_tests' in sys.modules


class BLEMeshRunner(MbedGreenteaMeshRunnerInterface):
    def __init__(self, options=None):
        MbedGreenteaMeshRunnerInterface.__init__(self, options=options)
        self.config = None
        self.benches = None

    def setup(self):
        # Read configuration for default config.json file
        gt_log("reading configuration from config.json")
        init_ret = self.read_config()
        if not init_ret:
            gt_log_err("can't read configuration under current location")
            return False

        # Check basic configuration settings
        gt_log("checking configuration...")
        config_ret = self.check_config()
        if config_ret:
            gt_log_tab("project '%s'"% self.config['project'])
            gt_log_tab("name '%s'"% self.config['name'])
            gt_log_tab("description '%s'"% self.config['description'])

        # Print configuration in verbose mode
        if self.options.verbose:
            gt_log("printing configuration...")
            self.print_config()

        # Check which bench configurations are correct
        gt_log("scanning for bench configurations...")
        scan_ret = self.scan_mesh_tests(verbose=self.options.verbose)
        
        # Auto-detect connected to host devices
        self.read_mbed_devices()

        return True
        
    def run(self):
        pass

    def read_config(self, config_name=None):
        result = None
        if not config_name:
            config_name = self.DEFAULT_CONFIG
        config_data = self.read_json_from_file(config_name, verbose=True)
        if config_data:
            self.config = config_data
            result = True
        return result

    def read_json_from_file(self, path, verbose=False):
        result = True
        try:
            with open(path) as f:
                result = json.load(f)
        except Exception as e:
            if verbose:
                gt_log_err(str(e))
            result = False
        return result
        
    def print_config(self):
        print json.dumps(self.config, indent=4)

    def check_config(self):
        result = False
        if "suite" not in self.config:
            gt_log_err("no 'suite' defined in config.json file")
        else:
            if "mbed-greentea" not in self.config['suite']:
                gt_log_err("configuration 'suite' ")
                gt_log_tab("available suites:")
                for suite in self.config['suite']:
                    gt_log_tab("suite '%s'"% suite)
            else:
                result = True
        return result

    def scan_mesh_tests(self, verbose=False):
        result = []
        faulty_benches = []
        pwd = '.'
        dirs = [os.path.join(pwd, o) for o in os.listdir(pwd) if os.path.isdir(os.path.join(pwd, o))]
        for d in dirs:
            bench_path = os.path.join(d, 'bench.json')
            bench_data = self.read_json_from_file(bench_path)
            if bench_data:
                gt_log_tab("found bench config under '%s'"% bench_path)
                result.append(d)
            else:
                faulty_benches.append(d)
    
        if verbose and faulty_benches:
            gt_log_warn("unknown bench configurations:")
            for d in faulty_benches:
                gt_log_tab("directory '%s'"% d)

        self.benches = result
        return not result        

    def read_mbed_devices(self):
        gt_log("auto-detecting connected devices...")
        self.mbeds = mbed_lstools.create()
        self.mbeds_list = self.mbeds.list_mbeds()
        self.platform_list = self.mbeds.list_platforms_ext()
        for mbed in self.platform_list:
            n = int(self.platform_list[mbed])
            gt_log_tab("found %d platform%s '%s'"% (n, '' if n==1 else 's', mbed))
        if not self.platform_list:
            gt_log_warn("failed to auto-detect any compatible device")
        
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
    mesh_runner = BLEMeshRunner(opts)
    if not mesh_runner.setup():
        return(-1);
        
    if not mesh_runner.run():
        return(-2)
        
    return(0)
