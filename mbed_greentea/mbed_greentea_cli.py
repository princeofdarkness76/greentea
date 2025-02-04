#!/usr/bin/env python

"""
mbed SDK
Copyright (c) 2011-2014 ARM Limited
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
import optparse
<<<<<<< HEAD
from time import time, sleep
from Queue import Queue
from threading import Thread


from mbed_greentea.mbed_test_api import run_host_test
from mbed_greentea.mbed_test_api import TEST_RESULTS
from mbed_greentea.mbed_test_api import TEST_RESULT_OK
from mbed_greentea.cmake_handlers import load_ctest_testsuite
from mbed_greentea.cmake_handlers import list_binaries_for_targets
from mbed_greentea.mbed_report_api import exporter_text
from mbed_greentea.mbed_report_api import exporter_json
from mbed_greentea.mbed_report_api import exporter_junit
from mbed_greentea.mbed_target_info import get_mbed_clasic_target_info
from mbed_greentea.mbed_target_info import get_mbed_target_from_current_dir
from mbed_greentea.mbed_greentea_log import gt_log
from mbed_greentea.mbed_greentea_log import gt_bright
from mbed_greentea.mbed_greentea_log import gt_log_tab
from mbed_greentea.mbed_greentea_log import gt_log_err
from mbed_greentea.mbed_greentea_dlm import GREENTEA_KETTLE_PATH
from mbed_greentea.mbed_greentea_dlm import greentea_get_app_sem
from mbed_greentea.mbed_greentea_dlm import greentea_update_kettle
from mbed_greentea.mbed_greentea_dlm import greentea_clean_kettle
from mbed_greentea.mbed_yotta_api import build_with_yotta
from mbed_greentea.mbed_greentea_hooks import GreenteaHooks
from mbed_greentea.mbed_yotta_target_parse import YottaConfig
=======
from time import time

from mbed_greentea import print_version
from mbed_test_api import run_host_test
from mbed_test_api import run_cli_command
from mbed_test_api import TEST_RESULTS
from mbed_test_api import TEST_RESULT_OK
from cmake_handlers import load_ctest_testsuite
from cmake_handlers import list_binaries_for_targets
from mbed_report_api import exporter_text
from mbed_report_api import exporter_json
from mbed_report_api import exporter_junit
from mbed_target_info import get_mbed_clasic_target_info
from mbed_target_info import get_mbed_supported_test
from mbed_target_info import get_mbed_target_from_current_dir
from mbed_greentea_log import gt_log
from mbed_greentea_log import gt_bright
from mbed_greentea_log import gt_log_tab
from mbed_greentea_log import gt_log_err
from mbed_greentea_dlm import GREENTEA_KETTLE_PATH
from mbed_greentea_dlm import greentea_get_app_sem
from mbed_greentea_dlm import greentea_update_kettle
from mbed_greentea_dlm import greentea_clean_kettle
from mbed_greentea_dlm import greentea_kettle_info
from mbed_greentea_dlm import greentea_release_target_id
from mbed_greentea_dlm import greentea_acquire_target_id_from_list
<<<<<<< HEAD

from mbedgt_meshtest import main_meshtest_cli
from mbedgt_singletest import main_singletest_cli
=======
>>>>>>> origin/devel_test_flow

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> ARMmbed/devel_ble_support
=======
>>>>>>> origin/devel_ble_support
=======
>>>>>>> origin/devel_ble_support

try:
    import mbed_lstools
    import mbed_host_tests
except ImportError as e:
    print str(e)

MBED_LMTOOLS = 'mbed_lstools' in sys.modules
MBED_HOST_TESTS = 'mbed_host_tests' in sys.modules

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
RET_NO_DEVICES = 1001
RET_YOTTA_BUILD_FAIL = -1
LOCAL_HOST_TESTS_DIR = './test/host_tests'  # Used by mbedhtrun -e <dir>

def get_local_host_tests_dir(path):
    """! Forms path to local host tests. Performs additional basic checks if directory exists etc.
    """
    # If specified path exist return path
    if path and os.path.exists(path) and os.path.isdir(path):
        return path
    # If specified path is not set or doesn't exist returns default path
    if not path and os.path.exists(LOCAL_HOST_TESTS_DIR) and os.path.isdir(LOCAL_HOST_TESTS_DIR):
        return LOCAL_HOST_TESTS_DIR
    return None

def print_version(verbose=True):
    """! Print current package version
    """
    import pkg_resources  # part of setuptools
    version = pkg_resources.require("mbed-greentea")[0].version
    if verbose:
        print version
    return version


def main():
    """ Closure for main_cli() function """
=======

def main():
=======
=======

def main():
    """ Closure for main_singletest_cli() function """
>>>>>>> origin/devel_ble_support

def main():
>>>>>>> origin/devel_ble_support
    """ Closure for main_singletest_cli() function """

>>>>>>> ARMmbed/devel_ble_support
    parser = optparse.OptionParser()

    parser.add_option('-t', '--target',
                    dest='list_of_targets',
                    help='You can specify list of targets you want to build. Use comma to sepatate them')

    parser.add_option('-n', '--test-by-names',
                    dest='test_by_names',
                    help='Runs only test enumerated it this switch. Use comma to separate test case names.')

    parser.add_option("-O", "--only-build",
                    action="store_true",
                    dest="only_build_tests",
                    default=False,
                    help="Only build repository and tests, skips actual test procedures (flashing etc.)")

    parser.add_option("", "--skip-build",
                    action="store_true",
                    dest="skip_yotta_build",
                    default=False,
                    help="Skip calling 'yotta build' on this module")

    copy_methods_str = "Plugin support: " + ', '.join(mbed_host_tests.host_tests_plugins.get_plugin_caps('CopyMethod'))
    parser.add_option("-c", "--copy",
                    dest="copy_method",
                    help="Copy (flash the target) method selector. " + copy_methods_str,
                    metavar="COPY_METHOD")

    parser.add_option('', '--parallel',
                    dest='parallel_test_exec',
                    default=1,
                    help='Experimental, you execute test runners for connected to your host MUTs in parallel (speeds up test result collection)')

    parser.add_option("-e", "--enum-host-tests",
                    dest="enum_host_tests",
                    help="Define directory with yotta module local host tests. Default: ./test/host_tests")

    parser.add_option('', '--config',
                    dest='verbose_test_configuration_only',
                    default=False,
                    action="store_true",
                    help='Displays connected boards and detected targets and exits.')

    parser.add_option('', '--release',
                    dest='build_to_release',
                    default=False,
                    action="store_true",
                    help='If possible force build in release mode (yotta -r).')

    parser.add_option('', '--debug',
                    dest='build_to_debug',
                    default=False,
                    action="store_true",
                    help='If possible force build in debug mode (yotta -d).')

    parser.add_option('', '--list',
                    dest='list_binaries',
                    default=False,
                    action="store_true",
                    help='List available binaries')

    parser.add_option('-m', '--map-target',
                    dest='map_platform_to_yt_target',
                    help='List of custom mapping between platform name and yotta target. Comma separated list of PLATFORM:TARGET tuples')

    parser.add_option('', '--use-tids',
                    dest='use_target_ids',
                    help='Specify explicitly which devices can be used by Greentea for testing by creating list of allowed Target IDs (use comma separated list)')

    parser.add_option('', '--lock',
                    dest='lock_by_target',
                    default=False,
                    action="store_true",
                    help='Use simple resource locking mechanism to run multiple application instances')

    parser.add_option('', '--use-tids',
                    dest='use_target_ids',
                    help='Specify explicitly which target IDs can be used by Greentea (use comma separated list)')

    parser.add_option('', '--digest',
                    dest='digest_source',
                    help='Redirect input from where test suite should take console input. You can use stdin or file name to get test case console output')

    parser.add_option('-H', '--hooks',
                    dest='hooks_json',
                    help='Load hooks used drive extra functionality')

    parser.add_option('', '--test-cfg',
                    dest='json_test_configuration',
                    help='Pass to host test data with host test configuration')

    parser.add_option('', '--mesh',
                    dest='mesh_test_module',
                    default=False,
                    action="store_true",
                    help='Check for mesh test description in current directory (config.json)')

    parser.add_option('', '--run',
                    dest='run_app',
                    help='Flash, reset and dump serial from selected binary application')

    parser.add_option('', '--report-junit',
                    dest='report_junit_file_name',
                    help='You can log test suite results in form of JUnit compliant XML report')

    parser.add_option('', '--report-text',
                    dest='report_text_file_name',
                    help='You can log test suite results to text file')

    parser.add_option('', '--report-json',
                    dest='report_json',
                    default=False,
                    action="store_true",
                    help='Outputs test results in JSON')

    parser.add_option('', '--report-fails',
                    dest='report_fails',
                    default=False,
                    action="store_true",
                    help='Prints console outputs for failed tests')

    parser.add_option('', '--yotta-registry',
                    dest='yotta_search_for_mbed_target',
                    default=False,
                    action="store_true",
                    help='Use on-line yotta registry to search for compatible with connected mbed devices yotta targets. Default: search is done in yotta_targets directory')

    parser.add_option('-V', '--verbose-test-result',
                    dest='verbose_test_result_only',
                    default=False,
                    action="store_true",
                    help='Prints test serial output')

    parser.add_option('-v', '--verbose',
                    dest='verbose',
                    default=False,
                    action="store_true",
                    help='Verbose mode (prints some extra information)')

    parser.add_option('', '--version',
                    dest='version',
                    default=False,
                    action="store_true",
                    help='Prints package version and exits')

    parser.description = """This automated test script is used to execute tests for yotta modules on mbed-enabled devices"""
    parser.epilog = """Example: mbedgt --target frdm-k64f-gcc"""

    (opts, args) = parser.parse_args()

    # Check for missing modules
    if not MBED_LMTOOLS:
        gt_log_err("error: mbed-ls proprietary module not installed")
        exit(-1)
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/devel_ble_support

    if not MBED_HOST_TESTS:
        gt_log_err("error: mbed-host-tests proprietary module not installed")
        exit(-1)
<<<<<<< HEAD

=======

    if not MBED_HOST_TESTS:
        gt_log_err("error: mbed-host-tests proprietary module not installed")
        exit(-1)

>>>>>>> origin/devel_ble_support
=======

>>>>>>> origin/devel_ble_support
    # Select which functionality will drive CLI
    if opts.mesh_test_module:
        main_cli = main_meshtest_cli
    else:
        main_cli = main_singletest_cli

    cli_ret = 0
    start = time()
    if opts.lock_by_target:
        # We are using Greentea proprietary locking mechanism to lock between platforms and targets
<<<<<<< HEAD
<<<<<<< HEAD
        gt_log("using (experimental) simple locking mechanism")
        gt_log_tab("kettle: %s"% GREENTEA_KETTLE_PATH)
=======
>>>>>>> ARMmbed/devel_test_flow
=======
>>>>>>> origin/devel_test_flow
        gt_file_sem, gt_file_sem_name, gt_instance_uuid = greentea_get_app_sem()
        gt_log("using (experimental) simple locking mechanism")
        gt_log_tab("kettle: %s"% GREENTEA_KETTLE_PATH)
        gt_log_tab("greentea lock uuid '%s'"% gt_instance_uuid)
        with gt_file_sem:
            greentea_update_kettle(gt_instance_uuid)
            try:
                cli_ret = main_cli(opts, args, gt_instance_uuid)
            except KeyboardInterrupt:
                greentea_clean_kettle(gt_instance_uuid)
                gt_log_err("ctrl+c keyboard interrupt!")
<<<<<<< HEAD
<<<<<<< HEAD
                return(-2)    # Keyboard interrupt
            except:
                greentea_clean_kettle(gt_instance_uuid)
                gt_log_err("unexpected error:")
                gt_log_tab(sys.exc_info()[0])
=======
                exit(-2)    # Keyboard interrupt
            except Exception as e:
                greentea_clean_kettle(gt_instance_uuid)
                gt_log_err("Unexpected error:")
                gt_log_tab(str(e))
                cli_ret = -3
>>>>>>> ARMmbed/devel_test_flow
=======
                exit(-2)    # Keyboard interrupt
            except Exception as e:
                greentea_clean_kettle(gt_instance_uuid)
                gt_log_err("Unexpected error:")
                gt_log_tab(str(e))
                cli_ret = -3
>>>>>>> origin/devel_test_flow
                raise
            greentea_clean_kettle(gt_instance_uuid)
    else:
        # Standard mode of operation
        # Other instance must provide mutually exclusive access control to platforms and targets
        try:
            cli_ret = main_cli(opts, args)
        except KeyboardInterrupt:
            gt_log_err("ctrl+c keyboard interrupt!")
<<<<<<< HEAD
            return(-2)    # Keyboard interrupt
        except Exception as e:
            gt_log_err("unexpected error:")
=======
            exit(-2)    # Keyboard interrupt
        except Exception as e:
            gt_log_err("Unexpected error:")
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> ARMmbed/devel_ble_support
=======
>>>>>>> origin/devel_ble_support
=======
>>>>>>> origin/devel_ble_support
            gt_log_tab(str(e))
            raise

    if not any([opts.list_binaries, opts.version]):
        print "completed in %.2f sec"% (time() - start)
    return(cli_ret)

def run_test_thread(test_result_queue, test_queue, opts, mut, mut_info, yotta_target_name, greentea_hooks):
    test_exec_retcode = 0
    test_platforms_match = 0
    test_report = {}
    yotta_config_baudrate = None    # Default serial port baudrate forced by configuration

    yotta_config = YottaConfig()
    yotta_config.init(yotta_target_name)

    yotta_config_baudrate = yotta_config.get_baudrate()

    while not test_queue.empty():
        try:
            test = test_queue.get(False)
        except Exception as e:
            print(str(e))
            break

        test_result = 'SKIPPED'

        disk = mut['mount_point']
        port = mut['serial_port']
        micro = mut['platform_name']
        program_cycle_s = mut_info['properties']['program_cycle_s']
        copy_method = opts.copy_method if opts.copy_method else 'shell'
        verbose = opts.verbose_test_result_only
        enum_host_tests_path = get_local_host_tests_dir(opts.enum_host_tests)

        # We will force configuration specific baudrate
        if port:
            port = "%s:%d"% (port, yotta_config_baudrate)

        test_platforms_match += 1
        #gt_log_tab("running host test...")
        host_test_result = run_host_test(test['image_path'],
                                         disk,
                                         port,
                                         micro=micro,
                                         copy_method=copy_method,
                                         program_cycle_s=program_cycle_s,
                                         digest_source=opts.digest_source,
                                         json_test_cfg=opts.json_test_configuration,
                                         enum_host_tests_path=enum_host_tests_path,
                                         verbose=verbose)

        single_test_result, single_test_output, single_testduration, single_timeout = host_test_result
        test_result = single_test_result

        build_path = os.path.join("./build", yotta_target_name)
        build_path_abs = os.path.abspath(build_path)

        if single_test_result != TEST_RESULT_OK:
            test_exec_retcode += 1
        else:
            if greentea_hooks and greentea_hooks.is_hooked_to('hook_test_end'):
                # Test was successful
                # We can execute test hook just after test is finished ('hook_test_end')
                format = {
                    "test_name": test['test_bin'],
                    "test_bin_name": os.path.basename(test['image_path']),
                    "image_path": test['image_path'],
                    "build_path": build_path,
                    "build_path_abs": build_path_abs,
                    "yotta_target_name": yotta_target_name,
                }
                gt_log("execute test end hook 'hook_test_end'")
                for k in format:
                    gt_log_tab("{%s} -> '%s'"% (k, format[k]))
                greentea_hooks.run_hook('hook_test_end', format)

        # Update report for optional reporting feature
        test_name = test['test_bin'].lower()
        if yotta_target_name not in test_report:
            test_report[yotta_target_name] = {}
        if test_name not in test_report[yotta_target_name]:
            test_report[yotta_target_name][test_name] = {}

        test_report[yotta_target_name][test_name]['single_test_result'] = single_test_result
        test_report[yotta_target_name][test_name]['single_test_output'] = single_test_output
        test_report[yotta_target_name][test_name]['elapsed_time'] = single_testduration
        test_report[yotta_target_name][test_name]['platform_name'] = micro
        test_report[yotta_target_name][test_name]['copy_method'] = copy_method
        test_report[yotta_target_name][test_name]['build_path'] = build_path
        test_report[yotta_target_name][test_name]['build_path_abs'] = build_path_abs
        test_report[yotta_target_name][test_name]['image_path'] = test['image_path']
        test_report[yotta_target_name][test_name]['test_bin_name'] = os.path.basename(test['image_path'])

        gt_log("test on hardware with target id: %s \n\ttest '%s' %s %s in %.2f sec"% (mut['target_id'], test['test_bin'], '.' * (80 - len(test['test_bin'])), test_result, single_testduration))

        if single_test_result != 'OK' and not verbose and opts.report_fails:
            # In some cases we want to print console to see why test failed
            # even if we are not in verbose mode
            gt_log_tab("test failed, reporting console output (specified with --report-fails option)")
            print
            print single_test_output

    #greentea_release_target_id(mut['target_id'], gt_instance_uuid)
    test_result_queue.put({'test_platforms_match': test_platforms_match,
                           'test_exec_retcode': test_exec_retcode,
                           'test_report': test_report})
    return

    """! This is main CLI function with all command line parameters
    @details This function also implements CLI workflow depending on CLI parameters inputed
    @return This function doesn't return, it exits to environment with proper success code
    """

    if not MBED_LMTOOLS:
        gt_log_err("error: mbed-ls proprietary module not installed")
        return (-1)

    if not MBED_HOST_TESTS:
        gt_log_err("error: mbed-host-tests proprietary module not installed")
        return (-1)

    # List available test binaries (names, no extension)
    if opts.list_binaries:
        list_binaries_for_targets()
        return (0)

    # Prints version and exits
    if opts.version:
        print_version()
        return (0)

    # We will load hooks from JSON file to support extra behaviour during test execution
    greentea_hooks = None
    if opts.hooks_json:
        greentea_hooks = GreenteaHooks(opts.hooks_json)

    # Capture alternative test console inputs, used e.g. in 'yotta test command'
    if opts.digest_source:
        enum_host_tests_path = get_local_host_tests_dir(opts.enum_host_tests)
        host_test_result = run_host_test(image_path=None,
                                         disk=None,
                                         port=None,
                                         digest_source=opts.digest_source,
                                         enum_host_tests_path=enum_host_tests_path,
                                         hooks=greentea_hooks,
                                         verbose=opts.verbose_test_result_only)

        single_test_result, single_test_output, single_testduration, single_timeout = host_test_result
        status = TEST_RESULTS.index(single_test_result) if single_test_result in TEST_RESULTS else -1
        return (status)

<<<<<<< HEAD
    ### Selecting yotta targets to process
    yt_targets = [] # List of yotta targets specified by user used to process during this run
    if opts.list_of_targets:
        yt_targets = opts.list_of_targets.split(',')
    else:
=======
    # mbed-enabled devices auto-detection procedures
    mbeds = mbed_lstools.create()
    mbeds_list = mbeds.list_mbeds_ext()

    # Option -t <opts.list_of_targets> supersedes yotta target set in current directory
    if opts.list_of_targets is None:
        if opts.verbose:
            gt_log("yotta target not set from command line (specified with -t option)")
>>>>>>> ARMmbed/devel_test_flow
        # Trying to use locally set yotta target
        gt_log("checking for yotta target in current directory")
        gt_log_tab("reason: no --target switch set")
        current_target = get_mbed_target_from_current_dir()
        if current_target:
            gt_log("assuming default target as '%s'"% gt_bright(current_target))
            # Assuming first target printed by 'yotta search' will be used
            yt_targets = [current_target]
        else:
            gt_log_tab("yotta target in current directory is not set")
            gt_log_err("yotta target is not specified. Use '%s' or '%s' command to set target"%
            (
                gt_bright('mbedgt -t <yotta_target>'),
                gt_bright('yotta target <yotta_target>')
            ))
            return (-1)

<<<<<<< HEAD
<<<<<<< HEAD
    #print "yt_targets:", yt_targets

    ### Query with mbedls for available mbed-enabled devices
    gt_log("detecting connected mbed-enabled devices...")

    # Detect devices connected to system
    mbeds = mbed_lstools.create()
    mbeds_list = mbeds.list_mbeds_ext()

    ready_mbed_devices = [] # Devices which can be used (are fully detected)

=======
=======
>>>>>>> origin/devel_test_flow
    unique_platforms = [] # Unique platforms names in detected set
    muts_info = {} # Platfrom: mut_info mapping
    platform_to_tids_map = {}    # platform_name : [tid, tid, tid, ...]

    gt_log("detecting connected mbed-enabled devices... %s"% ("no devices detected" if not len(mbeds_list) else ""))
>>>>>>> ARMmbed/devel_test_flow
    if mbeds_list:
        # Detect devices connected to system
        gt_log("detected %d device%s"% (len(mbeds_list), 's' if len(mbeds_list) != 1 else ''))
        for mut in mbeds_list:
<<<<<<< HEAD
<<<<<<< HEAD
            if not all(mut.values()):
                gt_log_err("can't detect all properties of the device!")
            else:
                ready_mbed_devices.append(mut)
                gt_log_tab("detected '%s' -> '%s', console at '%s', mounted at '%s', target id '%s'"% (
                    gt_bright(mut['platform_name']),
                    gt_bright(mut['platform_name_unique']),
                    gt_bright(mut['serial_port']),
                    gt_bright(mut['mount_point']),
                    gt_bright(mut['target_id'])
                ))
=======
            platform_text = gt_bright(mut['platform_name'])
            platform_unique_text = gt_bright(mut['platform_name_unique'])
            serial_text = gt_bright(mut['serial_port'])
            mount_text = gt_bright(mut['mount_point'])
            target_id_text = gt_bright(mut['target_id'])
            if not all([mut['platform_name'], mut['serial_port'], mut['mount_point']]):
                gt_log_err("can't detect all properties of the device!")
            gt_log_tab("detected '%s' -> '%s', console at '%s', mounted at '%s', target id '%s'"%
                (platform_text,
                 platform_unique_text,
                 serial_text,
                 mount_text,
                 target_id_text))

            # Determine unique platform set available
            if mut['platform_name'] not in unique_platforms:
                unique_platforms.append(mut['platform_name'])

            # Build platform_name => all platform target_ids mapping
            if mut['platform_name'] not in platform_to_tids_map:
                platform_to_tids_map[mut['platform_name']] = []
            platform_to_tids_map[mut['platform_name']].append(mut['target_id'])
>>>>>>> origin/devel_test_flow
    else:
        gt_log("no devices detected")
        return (RET_NO_DEVICES)

    ### Use yotta to search mapping between platform names and available platforms
    # Convert platform:target, ... mapping to data structure
    map_platform_to_yt_target = {}
    if opts.map_platform_to_yt_target:
        gt_log("user defined platform -> target supported mapping definition (specified with --map-target switch)")
        p_to_t_mappings = opts.map_platform_to_yt_target.split(',')
        for mapping in p_to_t_mappings:
            if len(mapping.split(':')) == 2:
                platform, yt_target = mapping.split(':')
                if platform not in map_platform_to_yt_target:
                    map_platform_to_yt_target[platform] = []
                map_platform_to_yt_target[platform].append(yt_target)
                gt_log_tab("mapped platform '%s' to be compatible with '%s'"% (
                    gt_bright(platform),
                    gt_bright(yt_target)
                ))
            else:
                gt_log_tab("unknown format '%s', use 'platform:target' format"% mapping)

    # Check if mbed classic target name can be translated to yotta target name

    mut_info_map = {}   # platform_name : mut_info_dict, extract yt_targets with e.g. [k["yotta_target"] for k in d['K64F']["yotta_targets"]]

    for mut in ready_mbed_devices:
        platfrom_name = mut['platform_name']
        if platfrom_name not in mut_info_map:
            mut_info = get_mbed_clasic_target_info(platfrom_name,
                                                   map_platform_to_yt_target,
                                                   use_yotta_registry=opts.yotta_search_for_mbed_target)
            if mut_info:
                mut_info_map[platfrom_name] = mut_info
    #print "mut_info_map:", json.dumps(mut_info_map, indent=2)

    ### List of unique ready platform names
    unique_mbed_devices = list(set(mut_info_map.keys()))
    #print "unique_mbed_devices", json.dumps(unique_mbed_devices, indent=2)

    ### Identify which targets has to be build because platforms are present
    yt_target_platform_map = {}     # yt_target_to_test : platforms to test on

    for yt_target in yt_targets:
        for platform_name in unique_mbed_devices:
            if yt_target in [k["yotta_target"] for k in mut_info_map[platform_name]["yotta_targets"]]:
                if yt_target not in yt_target_platform_map:
                    yt_target_platform_map[yt_target] = []
                if platform_name not in yt_target_platform_map[yt_target]:
                    yt_target_platform_map[yt_target].append(platform_name)
    #print "yt_target_platform_map", json.dumps(yt_target_platform_map, indent=2)

    ### We can filter in only specific target ids
    accepted_target_ids = None
    if opts.use_target_ids:
        gt_log("filtering out target ids not on below list (specified with --use-tids switch)")
        accepted_target_ids = opts.use_target_ids.split(',')
        for tid in accepted_target_ids:
            gt_log_tab("accepting target id '%s'"% gt_bright(tid))
=======
            platform_text = gt_bright(mut['platform_name'])
            platform_unique_text = gt_bright(mut['platform_name_unique'])
            serial_text = gt_bright(mut['serial_port'])
            mount_text = gt_bright(mut['mount_point'])
            target_id_text = gt_bright(mut['target_id'])
            if not all([mut['platform_name'], mut['serial_port'], mut['mount_point']]):
                gt_log_err("can't detect all properties of the device!")
            gt_log_tab("detected '%s' -> '%s', console at '%s', mounted at '%s', target id '%s'"%
                (platform_text,
                 platform_unique_text,
                 serial_text,
                 mount_text,
                 target_id_text))

            # Determine unique platform set available
            if mut['platform_name'] not in unique_platforms:
                unique_platforms.append(mut['platform_name'])

            # Build platform_name => all platform target_ids mapping
            if mut['platform_name'] not in platform_to_tids_map:
                platform_to_tids_map[mut['platform_name']] = []
            platform_to_tids_map[mut['platform_name']].append(mut['target_id'])
    else:
        gt_log("no devices detected")

    # Preload info about muts and available targets
    for unique_platform in unique_platforms:
        # Check if mbed classic target name can be translated to yotta target name
        gt_log("scan available targets for '%s' platform..."% gt_bright(unique_platform))
        muts_info[unique_platform] = get_mbed_clasic_target_info(unique_platform)

    # Preload info about muts and available targets
    for unique_platform in unique_platforms:
        # Check if mbed classic target name can be translated to yotta target name
        gt_log("scan available targets for '%s' platform..."% gt_bright(unique_platform))
        muts_info[unique_platform] = get_mbed_clasic_target_info(unique_platform)

    list_of_targets = opts.list_of_targets.split(',') if opts.list_of_targets is not None else None

    test_report = {}    # Test report used to export to Junit, HTML etc...

    if opts.list_of_targets is None:
        gt_log("assuming default target as '%s'"% gt_bright(current_target))
        gt_log_tab("reason: no --target switch set")
        list_of_targets = [current_target]
>>>>>>> ARMmbed/devel_test_flow

    test_exec_retcode = 0       # Decrement this value each time test case result is not 'OK'
    test_platforms_match = 0    # Count how many tests were actually ran with current settings
    target_platforms_match = 0  # Count how many platforms were actually tested with current settings

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    test_report = {}            # Test report used to export to Junit, HTML etc...
    muts_to_test = []           # MUTs to actually be tested
    test_queue = Queue()        # contains information about test_bin and image_path for each test case
    test_result_queue = Queue() # used to store results of each thread
    execute_threads = []        # list of threads to run test cases
=======
        # Check if mbed classic target name can be translated to yotta target name
        mut_info = get_mbed_clasic_target_info(mut['platform_name'])
        if mut_info is None:
            print "mbed-ls: mbed classic target name '%s' is not in target database"% (mut['platform_name'])
        else:
            print "mbedgt: scan available targets..."
            for yotta_target in mut_info['yotta_targets']:
                yotta_target_name = yotta_target['yotta_target']
                yotta_target_toolchain = yotta_target['mbed_toolchain']
>>>>>>> ARMmbed/testing

    ### check if argument of --parallel mode is a integer and greater or equal 1
    try:
        parallel_test_exec = int(opts.parallel_test_exec)
        if parallel_test_exec < 1:
            parallel_test_exec = 1
    except ValueError:
        gt_log_err("argument of mode --parallel is not a int, disable parallel mode")
        parallel_test_exec = 1


    ### Testing procedures, for each target, for each target's compatible platform
    for yotta_target_name in yt_target_platform_map:
        gt_log("processing '%s' yotta target compatible platforms..."% gt_bright(yotta_target_name))

        for platform_name in yt_target_platform_map[yotta_target_name]:
            gt_log("processing '%s' platform..."% gt_bright(platform_name))

            ### Select MUTS to test from list of available MUTS to start testing
            mut = None
            number_of_parallel_instances = 1
            for mbed_dev in ready_mbed_devices:
                if accepted_target_ids and mbed_dev['target_id'] not in accepted_target_ids:
                    continue

                if mbed_dev['platform_name'] == platform_name:
                    mut = mbed_dev
                    muts_to_test.append(mbed_dev)
                    gt_log("using platform '%s' for test:"% gt_bright(platform_name))
                    for k in mbed_dev:
                        gt_log_tab("%s = '%s'"% (k, mbed_dev[k]))
                    if number_of_parallel_instances < parallel_test_exec:
                        number_of_parallel_instances += 1
                    else:
                        break

            # Configuration print mode:
            if opts.verbose_test_configuration_only:
                continue

            if mut:
                target_platforms_match += 1
=======
    user_target_ids = opts.use_target_ids.split(',') if opts.use_target_ids else []  # User specific target IDs subset to use

=======
    user_target_ids = opts.use_target_ids.split(',') if opts.use_target_ids else []  # User specific target IDs subset to use

>>>>>>> origin/devel_test_flow
    # Configuration print only
    if opts.verbose_test_configuration_only:
        return (test_exec_retcode)

    muts_to_test = [] # MUTs to actually be tested

    gt_log("filtering out target ids not on below list (switch --use-tids)")
    for utids in user_target_ids:
        gt_log_tab("using only '%s'"% gt_bright(utids))

    # Selecting muts to be used for specific platform occurrence
    if opts.lock_by_target:
        temp_unique_platforms = set(unique_platforms)
        gt_log("locking required platforms (switch --lock)")
        if user_target_ids:
            gt_log("filtering out target ids not on below list (switch --use-tids)")
            for utids in user_target_ids:
                gt_log_tab("using only '%s'"% gt_bright(utids))
        for unique_platform in temp_unique_platforms:
            gt_log("locking required platform '%s'"% gt_bright(unique_platform))
            possible_target_ids = platform_to_tids_map[unique_platform]
            if possible_target_ids:
                if user_target_ids:
                    # Remove from possible_target_ids elements not on user_target_ids
                    possible_target_ids = [item for item in possible_target_ids if item in user_target_ids]
                for ptid in possible_target_ids:
                    gt_log_tab("available target '%s'"% gt_bright(ptid))
                locked_target_id = greentea_acquire_target_id_from_list(possible_target_ids, gt_instance_uuid)
                if locked_target_id:
                    gt_log_tab("locking platform '%s'"% gt_bright(locked_target_id))
                    for mut in mbeds_list:
                        if mut['platform_name'] == unique_platform:
                            if mut['target_id'] == locked_target_id:
                                mut_info = muts_info[mut['platform_name']]
                                if mut_info:
                                    for yotta_target in mut_info['yotta_targets']:
                                        yotta_target_name = yotta_target['yotta_target']
                                        # Add MUT to list of muts under test in this run
                                        if yotta_target_name in list_of_targets:
                                            target_platforms_match += 1
                                            muts_to_test.append(mut)
                                            gt_log_tab("locked '%s' -> '%s', target_id: '%s'"%
                                                (gt_bright(mut['platform_name']),
                                                 gt_bright(mut['platform_name_unique']),
                                                 gt_bright(mut['target_id'])))
                    if target_platforms_match == 0:
                        gt_log_tab("no platforms locked"% unique_platform)
                else:
                    gt_log_tab("failed to lock platform")
                    print greentea_kettle_info()
            else:
                gt_log_tab("no platform '%s' available to lock"% unique_platform)
                print greentea_kettle_info()
    else:
        temp_unique_platforms = set(unique_platforms)
        for mut in mbeds_list:
            # Use only target ids specified with --use-tids switch
            if user_target_ids:
                if mut['target_id'] not in user_target_ids:
                    gt_log_tab("skipped '%s'"% gt_bright(mut['target_id']))
                    continue
>>>>>>> ARMmbed/devel_test_flow

<<<<<<< HEAD
            if mut['platform_name'] in temp_unique_platforms:
                temp_unique_platforms.remove(mut['platform_name'])
                mut_info = muts_info[mut['platform_name']]
                if mut_info:
                    for yotta_target in mut_info['yotta_targets']:
                        yotta_target_name = yotta_target['yotta_target']
                        # Add MUT to list of muts under test in this run
                        if yotta_target_name in list_of_targets:
                            target_platforms_match += 1
                            muts_to_test.append(mut)
                            gt_log_tab("using '%s' -> '%s', target_id: '%s'"%
                                (gt_bright(mut['platform_name']),
                                 gt_bright(mut['platform_name_unique']),
                                 gt_bright(mut['target_id'])))

    # We can continue with testing because we actually have platforms to test
    if muts_to_test:
        for yotta_target in mut_info['yotta_targets']:
            yotta_target_name = yotta_target['yotta_target']

            for mut in muts_to_test:
                mut_info = muts_info[mut['platform_name']]

            if mut['platform_name'] in temp_unique_platforms:
                temp_unique_platforms.remove(mut['platform_name'])
                mut_info = muts_info[mut['platform_name']]
                if mut_info:
                    for yotta_target in mut_info['yotta_targets']:
                        yotta_target_name = yotta_target['yotta_target']
                        # Add MUT to list of muts under test in this run
                        if yotta_target_name in list_of_targets:
                            target_platforms_match += 1
                            muts_to_test.append(mut)
                            gt_log_tab("using '%s' -> '%s', target_id: '%s'"%
                                (gt_bright(mut['platform_name']),
                                 gt_bright(mut['platform_name_unique']),
                                 gt_bright(mut['target_id'])))

    # We can continue with testing because we actually have platforms to test
    if muts_to_test:
        for yotta_target in mut_info['yotta_targets']:
            yotta_target_name = yotta_target['yotta_target']

            for mut in muts_to_test:
                mut_info = muts_info[mut['platform_name']]

                # Demo mode: --run implementation (already added --run to mbedhtrun)
                # We want to pass file name to mbedhtrun (--run NAME  =>  -f NAME_ and run only one binary
                if opts.run_app:
                    gt_log("running '%s' for '%s'"% (gt_bright(opts.run_app), gt_bright(yotta_target_name)))
                    disk = mut['mount_point']
                    port = mut['serial_port']
                    micro = mut['platform_name']
                    program_cycle_s = mut_info_map[platfrom_name]['properties']['program_cycle_s']
                    copy_method = opts.copy_method if opts.copy_method else 'shell'
                    enum_host_tests_path = get_local_host_tests_dir(opts.enum_host_tests)

                    yotta_config = YottaConfig()
                    yotta_config.init(yotta_target_name)

                    yotta_config_baudrate = yotta_config.get_baudrate()

                    # We will force configuration specific baudrate
                    if port:
                        port = "%s:%d"% (port, yotta_config_baudrate)

                    test_platforms_match += 1
                    host_test_result = run_host_test(opts.run_app,
                                                     disk,
                                                     port,
                                                     micro=micro,
                                                     copy_method=copy_method,
                                                     program_cycle_s=program_cycle_s,
                                                     digest_source=opts.digest_source,
                                                     json_test_cfg=opts.json_test_configuration,
                                                     run_app=opts.run_app,
                                                     enum_host_tests_path=enum_host_tests_path,
                                                     verbose=True)

                    single_test_result, single_test_output, single_testduration, single_timeout = host_test_result
                    status = TEST_RESULTS.index(single_test_result) if single_test_result in TEST_RESULTS else -1
                    if single_test_result != TEST_RESULT_OK:
                        test_exec_retcode += 1
                    continue

                # Regression test mode:
                # Building sources for given target and perform normal testing

                yotta_result, yotta_ret = True, 0   # Skip build and assume 'yotta build' was successful
                if opts.skip_yotta_build:
                    gt_log("skipping calling yotta (specified with --skip-build option)")
                else:
                    yotta_result, yotta_ret = build_with_yotta(yotta_target_name,
                        verbose=opts.verbose,
                        build_to_release=opts.build_to_release,
                        build_to_debug=opts.build_to_debug)

                # We need to stop executing if yotta build fails
                if not yotta_result:
                    gt_log_err("yotta returned %d"% yotta_ret)
                    return (RET_YOTTA_BUILD_FAIL)

                if opts.only_build_tests:
                    continue

                # Build phase will be followed by test execution for each target
                if yotta_result and not opts.only_build_tests:
                    binary_type = mut_info_map[platform_name]['properties']['binary_type']
                    ctest_test_list = load_ctest_testsuite(os.path.join('.', 'build', yotta_target_name),
                        binary_type=binary_type)
                    #print json.dumps(ctest_test_list, indent=2)
                    #TODO no tests to execute

                filtered_ctest_test_list = ctest_test_list
                test_list = None
                if opts.test_by_names:
                    filtered_ctest_test_list = {}   # Subset of 'ctest_test_list'
                    test_list = opts.test_by_names.split(',')
                    gt_log("test case filter (specified with -n option)")

                    invalid_test_names = False
                    for test_name in test_list:
                        if test_name not in ctest_test_list:
                            gt_log_tab("test name '%s' not found in CTestTestFile.cmake (specified with -n option)"% gt_bright(test_name))
                            invalid_test_names = True
                        else:
<<<<<<< HEAD
                            gt_log_tab("test filtered in '%s'"% gt_bright(test_name))
                            filtered_ctest_test_list[test_name] = ctest_test_list[test_name]
                    if invalid_test_names:
                        gt_log("invalid test case names (specified with -n option)")
                        gt_log_tab("note: test case names are case sensitive")
                        gt_log_tab("note: see list of available test cases below")
                        list_binaries_for_targets(verbose_footer=False)

                gt_log("running %d test%s for target '%s' and platform '%s'"% (
                    len(filtered_ctest_test_list),
                    "s" if len(filtered_ctest_test_list) != 1 else "",
                    gt_bright(yotta_target_name),
                    gt_bright(platform_name)
                ))

                for test_bin, image_path in filtered_ctest_test_list.iteritems():
                    test = {"test_bin":test_bin, "image_path":image_path}
                    test_queue.put(test)

                number_of_threads = 0
                for mut in muts_to_test:
                    #################################################################
                    # Experimental, parallel test execution
                    #################################################################
                    if number_of_threads < parallel_test_exec:
                        args = (test_result_queue, test_queue, opts, mut, mut_info, yotta_target_name, greentea_hooks)
                        t = Thread(target=run_test_thread, args=args)
                        execute_threads.append(t)
                        number_of_threads += 1

            ####

    gt_log_tab("use %s instance%s for testing" % (len(execute_threads), 's' if len(execute_threads) != 1 else ''))
    for t in execute_threads:
        t.daemon = True
        t.start()
    while test_result_queue.qsize() != len(execute_threads):
        sleep(1)

    # merge partial test reports from diffrent threads to final test report
    for t in execute_threads:
        t.join()
        test_return_data = test_result_queue.get(False)
        test_platforms_match += test_return_data['test_platforms_match']
        test_exec_retcode += test_return_data['test_exec_retcode']
        partial_test_report = test_return_data['test_report']
        # todo: find better solution, maybe use extend
        for report_key in partial_test_report.keys():
            if report_key not in test_report:
                test_report[report_key] = {}
                test_report.update(partial_test_report)
            else:
                test_report[report_key].update(partial_test_report[report_key])
=======
                            gt_log_err("yotta build failed!")
                    else:
                        gt_log("skipping calling yotta (specified with --skip-build option)")
                        yotta_result, yotta_ret = True, 0   # Skip build and assume 'yotta build' was successful

=======
>>>>>>> origin/testing
                    print "mbedgt: yotta build %s"% ('successful' if yotta_result else 'failed')
                    # Build phase will be followed by test execution for each target
                    if yotta_result and not opts.only_build_tests:
                        binary_type = mut_info['properties']['binary_type']
                        ctest_test_list = load_ctest_testsuite(os.path.join('.', 'build', yotta_target_name),
                            binary_type=binary_type)

<<<<<<< HEAD
                        test_list = None
                        if opts.test_by_names:
                            test_list = opts.test_by_names.split(',')
                            gt_log("test case filter: %s (specified with -n option)"% ', '.join(["'%s'"% gt_bright(t) for t in test_list]))

                            invalid_test_names = False
                            for test_n in test_list:
                                if test_n not in ctest_test_list:
                                    gt_log_tab("test name '%s' not found in CTestTestFile.cmake (specified with -n option)"% gt_bright(test_n))
                                    invalid_test_names = True
                            if invalid_test_names:
                                gt_log("invalid test case names (specified with -n option)")
                                gt_log_tab("note: test case names are case sensitive")
                                gt_log_tab("note: see list of available test cases below")
                                list_binaries_for_targets(verbose_footer=False)

                        gt_log("running tests for target '%s'" % gt_bright(yotta_target_name))
=======
                        print "mbedgt: running tests for '%s' target" % yotta_target_name
                        test_list = None
                        if opts.test_by_names:
                            test_list = opts.test_by_names.lower().split(',')
                            print "mbedgt: test case filter: %s (specified with -n option)" % ', '.join(["'%s'"% t for t in test_list])

                            for test_n in test_list:
                                if test_n not in ctest_test_list:
                                    print "\ttest name '%s' not found (specified with -n option)"% test_n

<<<<<<< HEAD
>>>>>>> ARMmbed/testing
=======
>>>>>>> origin/testing
                        for test_bin, image_path in ctest_test_list.iteritems():
                            test_result = 'SKIPPED'
                            # Skip test not mentioned in -n option
                            if opts.test_by_names:
<<<<<<< HEAD
<<<<<<< HEAD
                                if test_bin not in test_list:
=======
=======
>>>>>>> origin/testing
                                if test_bin.lower() not in test_list:
>>>>>>> ARMmbed/testing
                                    continue

                            if get_mbed_supported_test(test_bin):
                                disk = mut['mount_point']
                                port = mut['serial_port']
                                micro = mut['platform_name']
                                program_cycle_s = mut_info['properties']['program_cycle_s']
                                copy_method = opts.copy_method if opts.copy_method else 'shell'
                                verbose = opts.verbose_test_result_only

                                test_platforms_match += 1
                                gt_log_tab("running host test...")
                                host_test_result = run_host_test(image_path,
                                                                 disk,
                                                                 port,
                                                                 micro=micro,
                                                                 copy_method=copy_method,
                                                                 program_cycle_s=program_cycle_s,
                                                                 digest_source=opts.digest_source,
                                                                 json_test_cfg=opts.json_test_configuration,
                                                                 verbose=verbose)

                                single_test_result, single_test_output, single_testduration, single_timeout = host_test_result
                                test_result = single_test_result
                                if single_test_result != TEST_RESULT_OK:
                                    test_exec_retcode += 1

                                # Update report for optional reporting feature
                                test_name = test_bin.lower()
                                if yotta_target_name not in test_report:
                                    test_report[yotta_target_name] = {}
                                if test_name not in test_report[yotta_target_name]:
                                    test_report[yotta_target_name][test_name] = {}

                                test_report[yotta_target_name][test_name]['single_test_result'] = single_test_result
                                test_report[yotta_target_name][test_name]['single_test_output'] = single_test_output
                                test_report[yotta_target_name][test_name]['elapsed_time'] = single_testduration
                                test_report[yotta_target_name][test_name]['platform_name'] = micro
                                test_report[yotta_target_name][test_name]['platform_name_unique'] = mut['platform_name_unique']
                                test_report[yotta_target_name][test_name]['copy_method'] = copy_method

                                if single_test_result != 'OK' and not verbose and opts.report_fails:
                                    # In some cases we want to print console to see why test failed
                                    # even if we are not in verbose mode
                                    gt_log_tab("test failed, reporting console output (specified with --report-fails option)")
                                    print
                                    print single_test_output

                                gt_log_tab("test '%s' %s %s in %.2f sec"% (test_bin, '.' * (80 - len(test_bin)), test_result, single_testduration))
                    # We need to stop executing if yotta build fails
                    if not yotta_result:
                        gt_log_err("yotta returned %d"% yotta_ret)
                        test_exec_retcode = -1
                        return (test_exec_retcode)
<<<<<<< HEAD
>>>>>>> ARMmbed/devel_test_flow
=======
>>>>>>> origin/devel_test_flow

    if opts.verbose_test_configuration_only:
        print
        print "Example: execute 'mbedgt --target=TARGET_NAME' to start testing for TARGET_NAME target"
        return (0)

    gt_log("all tests finished!")

    # We will execute post test hooks on tests
    for yotta_target in test_report:
        for test_name in test_report[yotta_target]:
            test = test_report[yotta_target][test_name]
            # Test was successful
            if test['single_test_result'] == 'OK':
                if greentea_hooks and greentea_hooks.is_hooked_to('hook_post_test_end'):
                    # We can execute this test hook just after all tests are finished ('hook_post_test_end')
                    format = {
                        "test_name": test_name,
                        "test_bin_name": test['test_bin_name'],
                        "image_path": test['image_path'],
                        "build_path": test['build_path'],
                        "build_path_abs": test['build_path_abs'],
                        "yotta_target_name": yotta_target,
                    }
                    gt_log("execute post test end hook 'hook_post_test_end'")
                    for k in format:
                        gt_log_tab("{%s} -> '%s'"% (k, format[k]))
                    greentea_hooks.run_hook('hook_post_test_end', format)


    # This tool is designed to work in CI
    # We want to return success codes based on tool actions,
    # only if testes were executed and all passed we want to
    # return 0 (success)
    if not opts.only_build_tests:
        # Reports (to file)
        if opts.report_junit_file_name:
            junit_report = exporter_junit(test_report)
            with open(opts.report_junit_file_name, 'w') as f:
                f.write(junit_report)
        if opts.report_text_file_name:
            gt_log("exporting to junit '%s'..."% gt_bright(opts.report_text_file_name))
            text_report, text_results = exporter_text(test_report)
            with open(opts.report_text_file_name, 'w') as f:
                f.write(text_report)

        # Reports (to console)
        if opts.report_json:
            # We will not print summary and json report together
            gt_log("json test report:")
            print exporter_json(test_report)
        else:
            # Final summary
            if test_report:
                gt_log("test report:")
                text_report, text_results = exporter_text(test_report)
                print text_report
                print
                print "Result: " + text_results

        # This flag guards 'build only' so we expect only yotta errors
        if test_platforms_match == 0:
            # No tests were executed
            gt_log("no platform/target matching tests were found!")
            test_exec_retcode += -10
        if target_platforms_match == 0:
            # No platforms were tested
            gt_log("no target matching platforms were found!")
            test_exec_retcode += -100

    return (test_exec_retcode)