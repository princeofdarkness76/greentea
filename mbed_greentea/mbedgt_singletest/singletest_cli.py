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

from mbed_greentea import print_version
from mbed_greentea.mbed_test_api import run_host_test
from mbed_greentea.mbed_test_api import run_cli_command
from mbed_greentea.mbed_test_api import TEST_RESULTS
from mbed_greentea.mbed_test_api import TEST_RESULT_OK
from mbed_greentea.cmake_handlers import load_ctest_testsuite
from mbed_greentea.cmake_handlers import list_binaries_for_targets
from mbed_greentea.mbed_report_api import exporter_text
from mbed_greentea.mbed_report_api import exporter_json
from mbed_greentea.mbed_report_api import exporter_junit
from mbed_greentea.mbed_target_info import get_mbed_clasic_target_info
from mbed_greentea.mbed_target_info import get_mbed_supported_test
from mbed_greentea.mbed_target_info import get_mbed_target_from_current_dir
from mbed_greentea.mbed_greentea_log import gt_log
from mbed_greentea.mbed_greentea_log import gt_bright
from mbed_greentea.mbed_greentea_log import gt_log_tab
from mbed_greentea.mbed_greentea_log import gt_log_err

try:
    import mbed_lstools
    import mbed_host_tests
except Exception as e:
    print str(e)

MBED_LMTOOLS = 'mbed_lstools' in sys.modules
MBED_HOST_TESTS = 'mbed_host_tests' in sys.modules


def main_singletest_cli(opts, args, gt_instance_uuid=None):
    """! This is main CLI function with all command line parameters
    @details This function also implements CLI workflow depending on CLI parameters inputed
    @return This function doesn't return, it exits to environment with proper success code
    """

    # List available test binaries (names, no extension)
    if opts.list_binaries:
        list_binaries_for_targets()
        return (0)

    # Prints version and exits
    if opts.version:
        print_version()
        return (0)

    # Capture alternative test console inputs, used e.g. in 'yotta test command'
    if opts.digest_source:
        host_test_result = run_host_test(image_path=None,
                                         disk=None,
                                         port=None,
                                         digest_source=opts.digest_source,
                                         verbose=opts.verbose_test_result_only)

        single_test_result, single_test_output, single_testduration, single_timeout = host_test_result
        status = TEST_RESULTS.index(single_test_result) if single_test_result in TEST_RESULTS else -1
        return (status)

    # mbed-enabled devices auto-detection procedures
    mbeds = mbed_lstools.create()
    mbeds_list = mbeds.list_mbeds()
    platform_list = mbeds.list_platforms_ext()

    # Option -t <opts.list_of_targets> supersedes yotta target set in current directory
    if opts.list_of_targets is None:
        if opts.verbose:
            gt_log("yotta target not set from command line (specified with -t option)")
        # Trying to use locally set yotta target
        current_target = get_mbed_target_from_current_dir()

        if current_target:
            gt_log("yotta target in current directory is set to '%s'"% gt_bright(current_target))
            # Assuming first target printed by 'yotta search' will be used
            opts.list_of_targets = current_target.split(',')[0]
        else:
            gt_log("yotta target in current directory is not set")
            gt_log_err("yotta target is not specified. Use '%s' or '%s' command to set target"%
            (
                gt_bright('mbedgt -t <target>'),
                gt_bright('yotta target <target>')
            ))
            return (-1)

    gt_log("detecting connected mbed-enabled devices... %s"% ("no devices detected" if not len(mbeds_list) else ""))
    if mbeds_list:
        gt_log("detected %d device%s"% (len(mbeds_list), 's' if len(mbeds_list) != 1 else ''))
    else:
        gt_log("no devices detected")

    list_of_targets = opts.list_of_targets.split(',') if opts.list_of_targets is not None else None

    test_report = {}    # Test report used to export to Junit, HTML etc...

    if opts.list_of_targets is None:
        gt_log("assuming default target as '%s'"% gt_bright(current_target))
        gt_log_tab("reason: no --target switch set")
        list_of_targets = [current_target]

    test_exec_retcode = 0       # Decrement this value each time test case result is not 'OK'
    test_platforms_match = 0    # Count how many tests were actually ran with current settings
    target_platforms_match = 0  # Count how many platforms were actually tested with current settings

    for mut in mbeds_list:
        platform_text = gt_bright(mut['platform_name'])
        serial_text = gt_bright(mut['serial_port'])
        mount_text = gt_bright(mut['mount_point'])
        platform_target_id = gt_bright(mut['target_id'])    # We can use it to do simple resource lock

        if not all([platform_text, serial_text, mount_text]):
            gt_log_err("can't detect all properties of the device!")
            gt_log_tab("detected '%s', console at '%s', mounted at '%s'"% (platform_text, serial_text, mount_text))
            continue

        gt_log_tab("detected '%s', console at '%s', mounted at '%s'"% (platform_text, serial_text, mount_text))

        # Check if mbed classic target name can be translated to yotta target name
        gt_log("scan available targets for '%s' platform..."% gt_bright(mut['platform_name']))
        mut_info = get_mbed_clasic_target_info(mut['platform_name'])

        if mut_info is not None:
            for yotta_target in mut_info['yotta_targets']:
                yotta_target_name = yotta_target['yotta_target']

                if yotta_target_name in list_of_targets:
                    target_platforms_match += 1

                # Configuration print mode:
                if opts.verbose_test_configuration_only:
                    continue

                # Demo mode: --run implementation (already added --run to mbedhtrun)
                # We want to pass file name to mbedhtrun (--run NAME  =>  -f NAME_ and run only one binary
                if opts.run_app and yotta_target_name in list_of_targets:
                    gt_log("running '%s' for '%s'"% (gt_bright(opts.run_app), gt_bright(yotta_target_name)))
                    disk = mut['mount_point']
                    port = mut['serial_port']
                    micro = mut['platform_name']
                    program_cycle_s = mut_info['properties']['program_cycle_s']
                    copy_method = opts.copy_method if opts.copy_method else 'shell'
                    verbose = opts.verbose_test_result_only

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
                                                     verbose=True)

                    single_test_result, single_test_output, single_testduration, single_timeout = host_test_result
                    status = TEST_RESULTS.index(single_test_result) if single_test_result in TEST_RESULTS else -1
                    if single_test_result != TEST_RESULT_OK:
                        test_exec_retcode += 1
                    continue

                # Regression test mode:
                # Building sources for given target and perform normal testing
                if yotta_target_name in list_of_targets:
                    gt_log("using '%s' target, prepare to build"% gt_bright(yotta_target_name))
                    cmd = ['yotta'] # "yotta %s --target=%s,* build"% (yotta_verbose, yotta_target_name)
                    if opts.verbose is not None: cmd.append('-v')
                    cmd.append('--target=%s,*' % yotta_target_name)
                    cmd.append('build')
                    if opts.build_to_release:
                        cmd.append('-r')
                    elif opts.build_to_debug:
                        cmd.append('-d')

                    if not opts.skip_yotta_build:
                        gt_log("building your sources and tests with yotta...")
                        gt_log_tab("calling yotta: %s"% " ".join(cmd))
                        yotta_result, yotta_ret = run_cli_command(cmd, shell=False, verbose=opts.verbose)
                        if yotta_result:
                            gt_log("yotta build for target '%s' was successful"% gt_bright(yotta_target_name))
                        else:
                            gt_log_err("yotta build failed!")
                    else:
                        gt_log("skipping calling yotta (specified with --skip-build option)")
                        yotta_result, yotta_ret = True, 0   # Skip build and assume 'yotta build' was successful

                    # Build phase will be followed by test execution for each target
                    if yotta_result and not opts.only_build_tests:
                        binary_type = mut_info['properties']['binary_type']
                        ctest_test_list = load_ctest_testsuite(os.path.join('.', 'build', yotta_target_name),
                            binary_type=binary_type)

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
                        for test_bin, image_path in ctest_test_list.iteritems():
                            test_result = 'SKIPPED'
                            # Skip test not mentioned in -n option
                            if opts.test_by_names:
                                if test_bin not in test_list:
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
        else:
            gt_log_err("mbed classic target name '%s' is not in target database"% gt_bright(mut['platform_name']))

    if opts.verbose_test_configuration_only:
        print
        print "Example: execute 'mbedgt --target=TARGET_NAME' to start testing for TARGET_NAME target"
        return (0)

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
            gt_log("test report:")
            text_report, text_results = exporter_text(test_report)
            print text_report
            print
            print "Result: " + text_results

        # This flag guards 'build only' so we expect only yotta errors
        if test_platforms_match == 0:
            # No tests were executed
            gt_log("no target matching tests were found!")
            test_exec_retcode += -10
        if target_platforms_match == 0:
            # No platforms were tested
            gt_log("no target matching platforms were found!")
            test_exec_retcode += -100

    return (test_exec_retcode)
