#!/usr/bin/env python3

import os
import subprocess
import sys

os.environ["LANGUAGE"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_CTYPE"] = "en_US.UTF-8"

if len(sys.argv) != 2:
    print("Usage: {} <manager-name>".format(sys.argv[0]))
    sys.exit(1)

DIRECTOR = sys.argv[1]

BASE_DIR = "/loc/{}".format(DIRECTOR)

ALL_BUGS = "{}/LoC-metrics.txt".format(BASE_DIR)
ALL_FW_BUGS = "{}/{}.txt".format(BASE_DIR, DIRECTOR)
ALL_OUT_BUGS = "{}/out-all-bugs.txt".format(BASE_DIR)

os.makedirs(BASE_DIR, exist_ok=True)
FW_QUERY = ""
FW_QUERY1 = ""

subprocess.run(["/ws/anbv-bgl/productivity/defect_metrics/underling_new.pl", "-l", DIRECTOR], stdout=open("/tmp/users_loc_{}.txt".format(DIRECTOR), "w"))

input_file = "/tmp/users_loc_{}.txt".format(DIRECTOR)

with open(input_file, "r") as file:
    for line in file:
        line = line.strip()
        engineer_total = 0

        # RMV123_BUGS = "{}/rmv123_{}.txt".format(BASE_DIR, line)
        # RMV_Query = "Engineer:{} and Status:R,M,V{{220801:}} and Project:CSC.labtrunk,CSC.sys and Status:R,M,V minus Status:R,M,V{{:220731}}".format(line)
        # print(RMV_Query)

        # subprocess.run(["/usr/cisco/bin/query.pl", RMV_Query], stdout=open(RMV123_BUGS, "a"))

        for bug_id in sys.stdin:
            bug_id = bug_id.strip()

            loc_count = 0
            comp_loc_count = 0
            loc_count_add = 0
            loc_count_mod = 0

            print("BUG ID -", bug_id)
            output = subprocess.run(["/usr/cisco/bin/dumpcr", "-e", "-a", "polaris_dev-code_reviews", bug_id], capture_output=True, text=True)
            lines = output.stdout.splitlines()

            for cr_line in lines:
                if "LoC:" in cr_line:
                    loc_count = int(cr_line.split()[1])
                    break

            if loc_count == 0:
                print("There is No LoC attachment")

                output = subprocess.run(["/usr/cisco/bin/dumpcr", "-t", bug_id], capture_output=True, text=True)
                diffs_lines = output.stdout.splitlines()

                comp_commit_file_name = None
                non_polaris_commit_file_name = None

                for diff_line in diffs_lines[::-1]:
                    if "Diffs-commit-comp" in diff_line:
                        comp_commit_file_name = diff_line.split()[0]
                        break
                    elif "Diffs-" in diff_line:
                        non_polaris_commit_file_name = diff_line.split()[0]
                        break

                if comp_commit_file_name is None:
                    print("This is NOT a Component Commit")

                    if non_polaris_commit_file_name is not None:
                        print("No Loc attachment and hence taking from NON Polaris diffs ::", non_polaris_commit_file_name)
                        output = subprocess.run(["/usr/cisco/bin/dumpcr", "-e", "-a", non_polaris_commit_file_name, bug_id], capture_output=True, text=True)
                        diff_lines = output.stdout.splitlines()

                        loc_count_add = sum([1 for diff_line in diff_lines if diff_line.startswith("+ ")])
                        loc_count_mod = sum([1 for diff_line in diff_lines if diff_line.startswith("- ")])
                        engineer_total += loc_count_add + loc_count_mod
                        with open("{}/{}_{}.txt".format(BASE_DIR, line, bug_id), "a") as bug_file:
                            bug_file.write("{}|{}|{}\n".format(line, loc_count_add, loc_count_mod))

                else:
                    print("This is IS a Component Commit")

                    print("No Loc attachment and hence taking from diffs")
                    output = subprocess.run(["/usr/cisco/bin/dumpcr", "-e", "-a", comp_commit_file_name, bug_id], capture_output=True, text=True)
                    diff_lines = output.stdout.splitlines()

                    loc_count_add = sum([1 for diff_line in diff_lines if diff_line.startswith("+ ")])
                    loc_count_mod = sum([1 for diff_line in diff_lines if diff_line.startswith("- ")])
                    engineer_total += loc_count_add + loc_count_mod
                    with open("{}/{}_{}.txt".format(BASE_DIR, line, bug_id), "a") as bug_file:
                        bug_file.write("{}|{}|{}\n".format(line, loc_count_add, loc_count_mod))

            else:
                print("The LoC Enclosure is available")
                print("The LOC from enclosure - ::{}::".format(loc_count))
                engineer_total += loc_count
                with open("{}/{}_{}.txt".format(BASE_DIR, line, bug_id), "a") as bug_file:
                    bug_file.write("{}|{}\n".format(line, loc_count))

            print("The TOTAL LOC:", engineer_total)

        print("For Engineer {}, the Total LoC: {}".format(line, engineer_total))
        with open(ALL_BUGS, "a") as all_bugs_file:
            all_bugs_file.write("{}|{}\n".format(line, engineer_total))

print("\nResults are at:\n")
print("ALL_BUGS=\"{}\"".format(ALL_BUGS))
