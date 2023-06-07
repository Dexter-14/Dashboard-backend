#!/usr/bin/env python3

import os
import sys

if len(sys.argv) != 2:
    print("Usage: {} <manager-name>".format(sys.argv[0]))
    sys.exit(1)
    

DIRECTOR = sys.argv[1]

BASE_DIR = "/auto/infra-devtest/anbv/scrubber/spollaka/9-Feb-2023/{}".format(DIRECTOR)

ALL_BUGS = "{}/all-metrics_{}.txt".format(BASE_DIR, DIRECTOR)
ALL_FW_BUGS = "{}/all-forwarded_bugs_{}.txt".format(BASE_DIR, DIRECTOR)
ALL_OUT_BUGS = "{}/out-all-bugs.txt".format(BASE_DIR)

os.makedirs(BASE_DIR, exist_ok=True)
FW_QUERY = ""
FW_QUERY1 = ""

with open("/tmp/users_{}.txt".format(DIRECTOR), "r") as f:
    for line in f:
        line = line.strip()
        RMV123_BUGS = "{}/rmv123_{}.txt".format(BASE_DIR, line)
        MGR_RMV123_BUGS = "{}/{}_rmv123.txt".format(BASE_DIR, DIRECTOR)
        RMV_Query = "Engineer:{} and Status:R,M,V{{220801:}} and Project:CSC.labtrunk,CSC.sys and Status:R,M,V minus Status:R,M,V{{:220731}}".format(line)
        print(RMV_Query)

        os.system("/usr/cisco/bin/query.pl '{}' >> '{}'".format(RMV_Query, RMV123_BUGS))
        rmv123_count = sum(1 for _ in open(RMV123_BUGS))
        os.system("/usr/cisco/bin/query.pl '{}' >> '{}'".format(RMV_Query, MGR_RMV123_BUGS))

        CJUD_BUGS = "{}/cjud_{}.txt".format(BASE_DIR, line)
        MGR_CJUD_BUGS = "{}/{}_cjud.txt".format(BASE_DIR, DIRECTOR)
        CJUD_Query = "Engineer:{} and Status:C,J,U,D{{220801:}} and Project:CSC.labtrunk,CSC.sys and Status:C,J,U,D".format(line)
        print(CJUD_Query)

        os.system("/usr/cisco/bin/query.pl '{}' >> '{}'".format(CJUD_Query, CJUD_BUGS))
        cjud_count = sum(1 for _ in open(CJUD_BUGS))
        os.system("/usr/cisco/bin/query.pl '{}' >> '{}'".format(CJUD_Query, MGR_CJUD_BUGS))

        Review_BUGS = "{}/review_{}.txt".format(BASE_DIR, line)
        Review_Query = "Code-reviewer:{} and Status:R,M,V{{220801:}} and Project:CSC.labtrunk,CSC.sys".format(line)
        print(Review_Query)

        os.system("/usr/cisco/bin/query.pl '{}' >> '{}'".format(Review_Query, Review_BUGS))
        review_count = sum(1 for _ in open(Review_BUGS))

        ALL_FW_BUGS = "{}/fw_{}.txt".format(BASE_DIR, line)
        FW_QUERY1 = "Fwd.*__2208.*__{}|Fwd.*__2209.*__{}|Fwd.*__2210.*__{}|Fwd.*__2211.*__{}|Fwd.*__2212.*__{}|Fwd.*__2301.*__{}|Fwd.*__2202.*__{}".format(line, line, line, line, line, line, line)
        print(FW_QUERY1)

        os.system("/usr/cisco/bin/query.pl '{}' >> '{}'".format(FW_QUERY1, ALL_FW_BUGS))
        fw_count = sum(1 for _ in open(ALL_FW_BUGS))

        with open(ALL_BUGS, "a") as f:
            f.write("{}|{}|{}|{}|{}|{}\n".format(DIRECTOR, line, rmv123_count, cjud_count, fw_count, review_count))

print("\nResults are at:\nALL_BUGS=\"{}\"".format(ALL_BUGS))
